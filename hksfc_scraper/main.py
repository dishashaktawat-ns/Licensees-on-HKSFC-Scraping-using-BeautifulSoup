from .individual_scraper import IndividualScraper
from .corporation_scraper import CorporateScraper
from .data_processing import normalize_and_check_schema
from .api_client import fetch_all
from .utils import generate_combinations
import pandas as pd
import csv


def run_scraper():
    individual_records = []
    corporate_records = []

    # Step 1: Fetch all base records
    for licstatus, role_type, ratype, letter in generate_combinations():
        try:
            records = fetch_all(licstatus, role_type, ratype, letter)

            for record in records:
                if record.get("isIndi") is True:
                    ind_scraper = IndividualScraper()
                    full_record = ind_scraper.get_full_record(record.get("ceref"))
                    if full_record:
                        individual_records.append(full_record)
                        # break
                else:
                    corp_scraper = CorporateScraper()
                    full_record = corp_scraper.get_full_corporate_record(record.get("ceref"))
                    if full_record:
                        corporate_records.append(full_record)
                        # break

        except Exception as e:
            print(
                f"Error fetching {licstatus}, {role_type}, ratype={ratype}, letter={letter}: {e}"
            )
            continue

    # Step 2: Normalize and validate schemas separately
    df_ind, schema_ind = normalize_and_check_schema(individual_records)
    df_corp, schema_corp = normalize_and_check_schema(corporate_records)

    # Step 3: Save to separate CSV files
    if not df_ind.empty:
        df_ind.to_csv(
            "hksfc_individuals.csv",
            index=False,
            encoding="utf-8-sig",
            quoting=csv.QUOTE_ALL,
            escapechar="\\",
        )
        print(f"Saved {len(df_ind)} individual records -> hksfc_individuals.csv")

    if not df_corp.empty:
        df_corp.to_csv(
            "hksfc_corporates.csv",
            index=False,
            encoding="utf-8-sig",
            quoting=csv.QUOTE_ALL,
            escapechar="\\",
        )
        print(f"Saved {len(df_corp)} corporate records -> hksfc_corporates.csv")

    print("\Scraping completed!")


if __name__ == "__main__":
    run_scraper()
