## std imports
from abc import (
  abstractclassmethod,
  abstractmethod
)
from cmath import e
from threading import Lock
from typing import final

## 3rd party imports
import networkx as nx

## custom imports
from registry.RegistryState import REGISTRY_STATE
from scooper.ScooperState import SCOOPER_STATE
from scoop_exception.RegistryEarlyRotationException import RegistryEarlyRotationException

class Registry: # this class is to be used by being extended
  def __init__(self, _entry_point, _driver) -> None:
    self.entry_point = _entry_point
    self.driver = _driver
    self.state_lock = Lock()
    self.state = REGISTRY_STATE.NOT_SET_UP
    self.location = None
    self.targets = []
    self.site_map = nx.DiGraph()

  @final
  def is_up_to_date(self):
    return not any(map(lambda targ: not targ.is_up_to_date()))

  @abstractmethod
  def get_tranche_of_targets(self, driver):
    raise NotImplementedError

  @final
  def register_target(self, _target):
    self.targets.append(_target)

  @final
  def select_target():


  @final
  def do_some_work(self, driver):
    if self.targets_cache:
      return self.targets_cache.pop() ## No work is done if we already have
                                      ## a target to return
    if self.state is REGISTRY_STATE.NOT_SET_UP:
      self.setup_state()
      self.transition_to_state(REGISTRY_STATE.SET_UP)
      return None, False

    elif self.state is REGISTRY_STATE.SET_UP:
      driver.get(self.entry_point)
      self.location = self.entry_point
      self.transition_to_state(REGISTRY_STATE.ENTRY_POINT)
      return None, False

    elif self.state is REGISTRY_STATE.ENTRY_POINT:
      self.current_target = self.select_target()
      if self.current_target is None:
        self.transition_to_state(REGISTRY_STATE.SET_UP)
        raise RegistryEarlyRotationException
      self.transition_to_state(REGISTRY_STATE.HOLDING_TARGET)
      return None, False

    elif self.state is REGISTRY_STATE.HOLDING_TARGET:
      try:
        self.current_target.nav_to_last_state(driver)
      except WebDriverException:
        pass
      self.transition_to_state(REGISTRY_STATE.POLLING_TARGET)
      return None, False

    elif self.state is REGISTRY_STATE.POLLING_TARGET:
      target, target_is_ready = self.current_target.poll()
      if not target_is_ready:
        self.transition_to_state(REGISTRY_STATE.SET_UP)
        return None, target_is_ready
      else:
        return target, target_is_ready

    '''
    if not self.targets_cache:
      self.get_tranche_of_targets(driver)
      self.to_next_tranche_of_targets(driver)
    '''
    return self.targets_cache.pop()

  @abstractmethod
  def to_next_tranche_of_targets(self, driver):
    raise NotImplementedError

  def transition_to_state(self, state):
    with self.state_lock:
      self.state = state

  def setup_state(self, driver):
    self.transition_to_state(REGISTRY_STATE.SET_UP)