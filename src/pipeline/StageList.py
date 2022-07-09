from .PipelineStage import PipelineStage
from typing import final

class StageList:
  def __init__(self, _pipeline) -> None:
    self.head = None
    self.pipeline = _pipeline

  @final
  def insert_stage(self, _fn):
    self.head = PipelineStage(
      _next = self.head,
      _cb = _fn,
      _pipeline = self.pipeline
    )