from scoop_exception.ScoopException import ScoopException


from ScoopException import ScoopException

class RegistryEarlyRotationException(ScoopException):
  def __init__(self):
    super().__init__("Registry forced early rotation")