import itertools
from .config import LICSTATUS_OPTIONS, ROLE_TYPE_OPTIONS, RATYPE_OPTIONS, NAME_START_LETTERS

def generate_combinations():
    """Yield all possible combinations"""
    return itertools.product(
        LICSTATUS_OPTIONS,
        ROLE_TYPE_OPTIONS,
        RATYPE_OPTIONS,
        NAME_START_LETTERS
    )
