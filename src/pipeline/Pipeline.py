from typing import final
import time
import sys
from threading import Lock

from .StageList import StageList
from .PipelineState import PIPELINE_STATE

from threading import Thread

class Pipeline: ## one difference between this and the unix model of a pipeline is that
  def __init__(self, _input = None) -> None: ## there isn't necessarily any notion of an output
    self.input        = _input
    self.state_lock   = Lock()
    self.state        = PIPELINE_STATE.IDLE
    self.stages       = StageList(self)
    self.input_thread = Thread(
      target = self.add_to_input_if_not_idle,
      args   = tuple(),
      daemon = True
    )

  @final
  def add_to_input_if_not_idle(self):
    while self.state is not PIPELINE_STATE.IDLE:
      item = self.input.get_item()
      self.stages.head.add_to_input(
        item
      )

  @final
  def add_stage(self, _fn):
    self.stages.insert_stage(_fn)

  @final
  def start(self):
    self.transition_to_state(PIPELINE_STATE.POLLING_INPUT)
    self.start_input_thread()
    cur = self.stages.head
    while cur is not None:
      cur.start_thread()
      cur = cur.next

  @final
  def start_input_thread(self):
    self.input_thread.start()

  @final
  def stop(self):
    self.transition_to_state(PIPELINE_STATE.IDLE)

  @final
  def transition_to_state(self, _state):
    with self.state_lock:
      self.state = _state
      ## call on-state callbacks

  def __str__(self):
    return str(self.stages.head)