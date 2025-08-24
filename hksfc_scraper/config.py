import string

BASE_URL = "https://apps.sfc.hk/publicregWeb/searchByRaJson"
INDIVIDUAL_BASE_URL = "https://apps.sfc.hk/publicregWeb/indi"
CORP_BASE_URL = "https://apps.sfc.hk/publicregWeb/corp"
API_KEY = "fc-a585b9eb73b44c579df04557dda5e5b7"


HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "application/json",
    "X-Requested-With": "XMLHttpRequest"
}

# All possible combinations
LICSTATUS_OPTIONS = ["active", "all"] 
ROLE_TYPE_OPTIONS = ["individual","corporation"] 
RATYPE_OPTIONS = list(range(1,2)) #list(range(1, 14)) + [101]
NAME_START_LETTERS = ['A'] #list(string.ascii_uppercase)
LIMIT = 20
INDI_DETAIL = ['details', 'addresses', 'conditions', 'disciplinaryAction', 'licenceRecord']