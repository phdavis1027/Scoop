from abc import abstractmethod
import os.path as path
import os
import sys
import random
import time
from typing import final
from threading import (
  Thread,
  Lock
)

from proton.reactor import Container
from seleniumwire import webdriver
from seleniumwire.webdriver import ChromeOptions

sys.path.append("..")
from utils.Headers import Headers
from scoop_exception.ScoopException import ScoopException
from scoop_exception.RegistryEarlyRotationException import (
  RegistryEarlyRotationException
)
from scooper.ScooperState import SCOOPER_STATE
from registry.Registry import Registry
from outpout.Output import Output

PROJECT_ROOT = path.join(path.dirname(__file__), path.join( os.pardir, os.pardir ))
BIN_PATH = path.join(PROJECT_ROOT, 'bin')

class Scooper:
  def __init__(
    self,
    _click_pattern = 1.2,
    _chromedriver_bin_path = path.join(BIN_PATH, 'chromedriver'),
    _browsermob_bin_path  = path.join(BIN_PATH, 'browsermob-proxy')
  ) -> None:
    self.state = SCOOPER_STATE.IDLE
    self.registries = []
    self.action_thread = None
    self.rotation_strategy = CircularRotationStrategy()
    self.click_pattern = _click_pattern
    self.chromedriver_bin_path = _chromedriver_bin_path
    self.browsermob_bin_path   = _browsermob_bin_path
    self.state_lock = Lock() ## lock to manage the global state object across threads
    self.outputs: list[Output] = []
    self.action_thread = Thread(
      target = self.pull,
      args = (),
      daemon = True
    )

  @final
  def plug_output(self, _output):
    self.outputs.append(_output)
    return self

  @final
  def setup_environment_variables(self):
    os.environ["PATH"] += self.chromedriver_bin_path
    os.environ["PATH"] += self.browsermob_bin_path
    print(os.environ["PATH"])

  @final
  def init(self):
    # set up selenium instance
    self.setup_environment_variables()
    self.browser = webdriver.Chrome(
      executable_path = self.chromedriver_bin_path
    )
    ## NEED TO DOCUMENT THIS CLEARLY
    self.browser.request_interceptor = Headers.default_request_headers
    return self

  @final
  def interceptor(self, _cb):
    self.browser.request_interceptor = _cb
    return self

  @final
  def start(self):
    self.transition_to_state(SCOOPER_STATE.SCOOPING)
    self.action_thread.start()
    self.action_thread.join()

  def register(self, registry):
    self.registries.append(registry)
    return self

  @final
  def pull(self):
    while self.state is not SCOOPER_STATE.SHUTTING_DOWN:
      current_registry = self.rotation_strategy(self.registries)
      if current_registry:
        try:
          while not current_registry.is_up_to_date():
            target, target_is_ready = current_registry.do_some_work(self.browser)
            if target_is_ready:
              for output in self.outputs:
                output.send(target)
        except RegistryEarlyRotationException:
          pass
      else:
        raise ScoopException

  @final
  def transition_to_state(self, _next_state):
    with self.state_lock:
      time.sleep(self.click_pattern)
      self.state = _next_state
      ### call _next_state callbacks

  @final
  def stop(self):
    self.transition_to_state(SCOOPER_STATE.SHUTTING_DOWN)
    return self

##============================================##
################################################
##============================================##
## Rotation Strategies

class RotationStrategy:
  def __init__(self) -> None:
    pass

  @abstractmethod
  def __call__(self, queue):
    raise NotImplementedError

class CircularRotationStrategy(RotationStrategy):
  def __call__(self, queue) -> Registry:
    if (queue):
      cur = queue.pop()
      queue.insert(0, cur)
      return cur
    return None

class RandomRotationStrategy(RotationStrategy):
  def __call__(self, queue):
    return random.choice(queue)