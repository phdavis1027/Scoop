class PipelineItem:
  def __init__(self, _payload, _final_stage) -> None:
    self.payload       = _payload
    self.current_stage = 0
    self.final_stage   = _final_stage