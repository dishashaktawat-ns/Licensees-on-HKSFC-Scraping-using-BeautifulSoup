# HKSFC Scraper

Public Register of Licensed Persons and Registered Institutions Scraper

This project extracts, transforms, and stores all licensees and registered institutions from the Hong Kong Securities and Futures Commission (HKSFC) public register. The pipeline handles both individual and corporation licensees, including license details and historical records.

## Table of Contents

* Core Requirements
* Package Structure
* Installation
* Usage
* Data Model
* Decisions and Trade-offs
* Demo
* Dependencies

## Package Structure

```
hksfc_scraper/
│
├── src/
│   ├── __init__.py
│   ├── config.py             # Constants like BASE_URL, HEADERS, etc.
│   ├── utils.py              # Helper functions
│   ├── api_client.py         # API fetching functions
│   ├── corporation_scraper.py# Corporation license details extraction
│   ├── individual_scraper.py # individual license details extraction
│   ├── transform.py          # Data normalization and validation
│   └── pipeline.py           # Main pipeline orchestrator
│
├── requirements.txt          # Dependencies
├── README.md
```

## Installation

1. Clone the repository:

```
git clone https://github.com/dishashaktawat-ns/Licensees-on-HKSFC-Scraping-using-BeautifulSoup.git
cd hksfc_scraper
```

2. Create a virtual environment (optional but recommended):

```
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

3. Install dependencies:

```
pip install -r requirements.txt
```

4. Optional: install as package:

```
pip install -e .
```

## Usage

### Run the pipeline

```
python -m hksfc_scraper.main
```

This will:

* Fetch all licensees (individuals and corporations)
* Handle pagination
* Normalize the JSON data

### Extract individual license details

```python
from src.selenium_scraper import extract_individual_details

ceref = "C12345"  # example license reference
details = extract_individual_details(ceref)
print(details)
```

## Data Model

The main CSV (sfc\_data\_all.csv) contains the following key fields:

| Field      | Description                                                    |
| ---------- | -------------------------------------------------------------- |
| ceref      | Unique license reference                                       |
| name       | Name of licensee / company                                     |
| licstatus  | License status (active or inactive)                            |
| roleType   | individual or corporation                                      |
| ratype     | License type code (1–13, 101)                                  |
| issuedDate | License issue date                                             |
| expiryDate | License expiry date                                            |
| …          | Additional fields from API (automatically detected and logged) |

## Decisions and Trade-offs

* Selenium is used only for extracting detailed individual license records due to dynamic table rendering on the website.
* Requests library handles main API ingestion (faster and lighter than Selenium).
* Schema drift detection ensures new or missing fields are logged without breaking the pipeline.
* Politeness: Added small delays to avoid overloading the HKSFC servers.
* CSV output chosen for simplicity and easy sharing. Can extend to databases later.
