import string

BASE_URL = "https://apps.sfc.hk/publicregWeb/searchByRaJson"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "application/json",
    "X-Requested-With": "XMLHttpRequest"
}

# All possible combinations
LICSTATUS_OPTIONS = ["active", "all"]
ROLE_TYPE_OPTIONS = ["individual", "corporation"]
RATYPE_OPTIONS = list(range(1, 14)) + [101]
NAME_START_LETTERS = list(string.ascii_uppercase)
LIMIT = 20
