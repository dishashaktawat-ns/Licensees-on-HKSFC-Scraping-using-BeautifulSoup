from typing import Type, Optional
from firecrawl import Firecrawl
from pydantic import BaseModel
from .schemas import CorporationLicenceSchema, CorporateDetailSchema, CorporationBusinessAddress
from .config import API_KEY, CORP_BASE_URL


class CorporateScraper:
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

    def extract_corporate_licences(self, corp_ce: str):
        url = f"{CORP_BASE_URL}/{corp_ce}/licences"
        return self.scrape_to_schema(url, CorporationLicenceSchema)

    def extract_corporate_addresses(self, corp_ce: str):
        url = f"{CORP_BASE_URL}/{corp_ce}/addresses"
        return self.scrape_to_schema(url, CorporationBusinessAddress)
    
    def extract_corporate_detail(self, corp_ce: str):
        url = f"{CORP_BASE_URL}/{corp_ce}/details"
        return self.scrape_to_schema(url, CorporateDetailSchema)
    

    # def extract_responsible_officers(self, corp_ce: str):
    #     url = f"{CORP_BASE_URL}/{corp_ce}/responsibleOfficers"
    #     return self.scrape_to_schema(url, CorporateROSchema)

    # def extract_representatives(self, corp_ce: str):
    #     url = f"{CORP_BASE_URL}/{corp_ce}/representatives"
    #     return self.scrape_to_schema(url, CorporateRepsSchema)

    # def extract_complaints_officers(self, corp_ce: str):
    #     url = f"{CORP_BASE_URL}/{corp_ce}/complaintsOfficers"
    #     return self.scrape_to_schema(url, CorporateCOOfficersSchema)

    # def extract_conditions(self, corp_ce: str):
    #     url = f"{CORP_BASE_URL}/{corp_ce}/conditions"
    #     return self.scrape_to_schema(url, CorporateConditionsSchema)

    # def extract_disciplinary_actions(self, corp_ce: str):
    #     url = f"{CORP_BASE_URL}/{corp_ce}/publicDisciplinaryActions"
    #     return self.scrape_to_schema(url, CorporateDisciplineSchema)

    # def extract_licence_record(self, corp_ce: str):
    #     url = f"{CORP_BASE_URL}/{corp_ce}/licenceRecord"
    #     return self.scrape_to_schema(url, CorporateLicenceRecordSchema)

    def get_full_corporate_record(self, corp_ce: str) -> dict:
        """
        Scrapes and consolidates all corporate data for the given CE number.
        """
        licences = self.extract_corporate_licences(corp_ce) or {}
        addresses = self.extract_corporate_addresses(corp_ce) or {}
        detail = self.extract_corporate_detail(corp_ce) or {}
        # ros = self.extract_responsible_officers(corp_ce) or {}
        # reps = self.extract_representatives(corp_ce) or {}
        # complaints = self.extract_complaints_officers(corp_ce) or {}
        # conditions = self.extract_conditions(corp_ce) or {}
        # disciplinary = self.extract_disciplinary_actions(corp_ce) or {}
        # record = self.extract_licence_record(corp_ce) or {}

        full_record = {
            "corporation_ce": corp_ce,
            "corporation_name": licences.get("corporation_name"),
            "detail": detail.get("detail"),
            "last_update": licences.get("last_update"),
            "licences": licences.get("licences", []),
            "addresses": addresses.get("addresses", []),
            # "responsible_officers": ros.get("officers", []),
            # "representatives": reps.get("representatives", []),
            # "complaints_officers": complaints.get("complaints_officers", []),
            # "conditions": conditions.get("conditions", []),
            # "public_disciplinary_actions": disciplinary.get("actions", []),
            # "licence_record_history": record.get("records", []),
            "remarks": licences.get("remarks", "")
        }

        return full_record
