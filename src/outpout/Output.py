from abc import abstractmethod

## the point of  this class is to get the message stored somewhere safe as
## quickly as possible

class Output:
  def __init__(self) -> None:
    raise NotImplementedError

  @abstractmethod
  def send(self, _target, _plugin_specific_params):
    raise NotImplementedError