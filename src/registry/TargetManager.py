import urllib

URL = urllib.ParseResult

class TargetManager:
  def __init__(self) -> None:
    self.last_known_state: URL = None