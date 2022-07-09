from abc import (
  abstractclassmethod,
  abstractmethod
)
from typing import final

class Registry: # this class is to be used by being extended
  def __init__(self, _entry_point) -> None:
    self.entry_point = _entry_point
    self.targets_cache = []

  @abstractmethod
  def target():
    raise NotImplementedError

  @abstractmethod
  def directions(driver):
    raise NotImplementedError

  @abstractmethod
  def is_up_to_date(_target):
    raise NotImplementedError

  @abstractmethod
  def get_tranche_of_targets(self, driver):
    raise NotImplementedError

  @final
  def get_target(self, driver):
    if not self.targets_cache:
      self.get_tranche_of_targets(driver)
      self.to_next_tranche_of_targets(driver)
    return self.targets_cache.pop()

  @abstractmethod
  def to_next_tranche_of_targets(self, driver):
    raise NotImplementedError


