from enum import Enum

class SCOOPER_STATE(Enum):
  IDLE = 1
  SCOOPING = 2
  SHUTTING_DOWN = 3
  ENGAGING_REGISTRY = 4 # strong guarantee is that if the the state is ENGAGING_REGISTRY,
                        # then there will be a current_registry defined; i.e.,
                        # the value will be truthy and will be able to call all
                        # the functions that a  registry can call
  ENTRY_POINT_PRE = 5
  ENTRY_POINT = 6