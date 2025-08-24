from typing import Type, Optional
from firecrawl import Firecrawl
from pydantic import BaseModel
from .config import INDIVIDUAL_BASE_URL, API_KEY
from .schemas import (
    LicenseesSchema,
    IndividualAddressesSchema,
    LicenseeRecord,
    IndividualDisciplinaryAction,
    IndividualConditions
)



class IndividualScraper:
    def __init__(self, api_key: str = API_KEY):
        self.app = Firecrawl(api_key=api_key)

    def scrape_to_schema(self, url: str, schema: Type[BaseModel]) -> Optional[dict]:
        """Generic Firecrawl scraper for structured data."""
        print(f"\n\n➡ Scraping: {url}")
        try:
            result = self.app.scrape(
                url,
                formats=[{"type": "json", "schema": schema}]
            )
            return result.json
        except Exception as e:
            import traceback
            traceback.print_exc()
            return None

    def extract_individual_details(self, ceref: str):
        url = f"{INDIVIDUAL_BASE_URL}/{ceref}/details"
        return self.scrape_to_schema(url, LicenseesSchema)

    def extract_individual_address(self, ceref: str):
        url = f"{INDIVIDUAL_BASE_URL}/{ceref}/addresses"
        return self.scrape_to_schema(url, IndividualAddressesSchema)

    def extract_individual_licence_record(self, ceref: str):
        url = f"{INDIVIDUAL_BASE_URL}/{ceref}/licenceRecord"
        return self.scrape_to_schema(url, LicenseeRecord)

    def extract_individual_disciplinary_action(self, ceref: str):
        url = f"{INDIVIDUAL_BASE_URL}/{ceref}/disciplinaryAction"
        return self.scrape_to_schema(url, IndividualDisciplinaryAction)

    def extract_individual_conditions(self, ceref: str):
        url = f"{INDIVIDUAL_BASE_URL}/{ceref}/conditions"
        return self.scrape_to_schema(url, IndividualConditions)

    def get_full_record(self, ceref: str) -> dict:
        """
        Collects and consolidates all scraped data into one JSON
        for the given individual (like we structured earlier).
        """
        details = self.extract_individual_details(ceref) or {}
        addresses = self.extract_individual_address(ceref) or {}
        licence_record = self.extract_individual_licence_record(ceref) or {}
        conditions = self.extract_individual_conditions(ceref) or {}
        disciplinary = self.extract_individual_disciplinary_action(ceref) or {}

        # --- Consolidate ---
        full_record = {
            "ceref": ceref,
            "name": details.get("name"),
            "chinese_name": details.get("chinese_name"),
            "date_of_licence": details.get("date_of_licence"),
            "last_update": details.get("last_update"),
            "licence_types": details.get("licence_types", []),
            "regulated_activities": details.get("regulated_activities", []),
            "addresses": addresses.get("addresses", []),
            "conditions": {
                "sfo_conditions": conditions.get("sfo_conditions", []),
                "amlo_conditions": conditions.get("amlo_conditions", [])
            },
            "disciplinary_actions": disciplinary.get("disciplinary_actions", []),
            "licence_record_history": licence_record.get("records", []),  # ⚠️ ensure schema aligns
            "remarks": details.get("remarks", "")
        }

        return full_record
