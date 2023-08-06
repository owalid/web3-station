from enum import Enum, EnumMeta

class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True

class BaseEnum(Enum, metaclass=MetaEnum):
    pass

class ALLOWED_ACTIONS(BaseEnum):
    deploy='0'
    faucet='1'
    validate='2'
    help='3'
    list='4'

class CHALLENGES(BaseEnum):
    cancunbeh='0'