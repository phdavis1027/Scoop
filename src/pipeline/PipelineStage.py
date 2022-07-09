from typing import final

from threading import (
  Lock,
  Thread
)

from pipeline.PipelineState import PIPELINE_STATE

class PipelineStage:
  def __init__(self, _next, _cb, _pipeline) -> None:
    self.next          = _next
    self.cb            = _cb
    self.inp           = []
    self.inp_lock      = Lock()
    self.pipeline      = _pipeline
    self.action_thread = Thread(
      target = self.process,
      args   = tuple(),
      daemon = True
    )

  @final
  def process(self):
    while True:
      self.process_one_item()

  @final
  def process_one_item(self):
    item = self.get_one_input_item() ## get some stuff out of the queue
    if item is not None:
      processed_item = self.cb(item)
      if self.next:
        self.next.add_to_input(processed_item)

  @final
  def get_one_input_item(self):
    if self.inp:
      item = self.inp.pop()
      return item

  @final
  def start_thread(self):
    self.action_thread.start()
    self.action_thread.join()

  @final
  def add_to_input(self, _payload):
    with self.inp_lock:
      self.inp.append(_payload)

  def __str__(self):
    return "[Pipeline stage: " + str(self.cb) + "] -> " + str(self.next)