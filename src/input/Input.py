from abc import abstractmethod
from typing import final

class Input:
  def __init__(self) -> None:
    self.input_queue = []

  @abstractmethod
  def init(self):
    raise NotImplementedError

  @final
  def get_item(self):
    if not self.input_queue:
      self.replenish_queue()
    if self.input_queue:
      return self.input_queue.pop()

  @abstractmethod
  def replenish_queue(self):
    raise NotImplementedError