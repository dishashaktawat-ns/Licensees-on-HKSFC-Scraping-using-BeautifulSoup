import requests
import time
import random
from .config import BASE_URL, HEADERS, LIMIT

def get_page(licstatus, role_type, ratype, name_start_letter, page=1, limit=LIMIT):
    """Fetch a single page of results"""
    params = {"_dc": str(int(time.time()*1000)) + str(random.randint(100,999))}
    form_data = {
        "licstatus": licstatus,
        "roleType": role_type,
        "ratype": str(ratype),
        "nameStartLetter": name_start_letter,
        "page": page,
        "start": (page - 1) * limit,
        "limit": limit,
    }

    res = requests.post(BASE_URL, params=params, data=form_data, headers=HEADERS, timeout=20)

    if res.status_code == 200:
        return res.json()
    else:
        return {"items": [], "totalCount": 0}


def fetch_all(licstatus, role_type, ratype, name_start_letter):
    """Fetch all pages for a given combination"""
    first_page = get_page(licstatus, role_type, ratype, name_start_letter)
    total_count = first_page.get("totalCount", 0)
    items = first_page.get("items", [])

    if total_count == 0:
        return []

    total_pages = (total_count // LIMIT) + (1 if total_count % LIMIT else 0)
    print(f"{licstatus}-{role_type}-ratype:{ratype}-letter:{name_start_letter} "
          f"Total records: {total_count} | Pages: {total_pages}")

    for page in range(2, total_pages + 1):
        time.sleep(0.5)
        data = get_page(licstatus, role_type, ratype, name_start_letter, page, LIMIT)
        items.extend(data.get("items", []))
        break

    return items
