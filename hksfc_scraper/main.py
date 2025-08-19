from .api_client import fetch_all
from .data_processing import normalize_and_check_schema
from .selenium_scraper import extract_individual_details
from .utils import generate_combinations
import csv

def run_scraper():
    all_records = []

    for licstatus, role_type, ratype, letter in generate_combinations():
        try:
            records = fetch_all(licstatus, role_type, ratype, letter)
            if records:
                all_records.extend(records)
                break
        except Exception as e:
            print(f"Error fetching {licstatus}, {role_type}, ratype={ratype}, letter={letter}: {e}")
            continue
    
    for record in all_records:
        if record.get('isIndi') is True:
            details = extract_individual_details(record.get('ceref'))
            record.update(details)
            break

    df, schema = normalize_and_check_schema(all_records)
    print("\n Scraping completed!")
    print("Total rows:", len(df))
    print("Columns:", df.columns.tolist())
    print(df.head())

    df.to_csv("hksfc_data.csv", index=False, encoding="utf-8-sig",
              quoting=csv.QUOTE_ALL, escapechar="\\")
    print("\n Data saved to sfc_data_all.csv")


if __name__ == "__main__":
    run_scraper()
