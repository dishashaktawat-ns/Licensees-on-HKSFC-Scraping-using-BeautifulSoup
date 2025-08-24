from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from datetime import date

#  Schemas for Individual Role type
class RegulatedActivity(BaseModel):
    principal: str = Field(description="Name of the principal institution, with code")
    date_of_accreditation: Optional[str] = Field(description="Date accredited to principal")
    regulated_activity: Optional[str] = Field(description="Type of regulated activity")
    effective_date: Optional[str] = Field(description="Effective date of activity")
    licence_role: Optional[str] = Field(description="Role of the licensee")
    remarks: Optional[str] = Field(description="Any remarks")


class AMLORecord(BaseModel):
    principal: Optional[str]
    date_of_accreditation: Optional[str]
    virtual_asset_service: Optional[str]
    effective_date: Optional[str]
    licence_role: Optional[str]
    remarks: Optional[str]


class LicenseesSchema(BaseModel):
    name: str = Field(description="Full English name of the licensee")
    chinese_name: Optional[str] = Field(description="Chinese name of the licensee")
    ceref: str = Field(description="Central Entity Reference number")
    licence_types: List[str] = Field(description="Types of licences held")
    
    # Under SFO
    date_of_licence: Optional[str]
    remarks: Optional[str]
    regulated_activities: List[RegulatedActivity] = []
    
    # Under AMLO
    amlo_records: List[AMLORecord] = []
    
    last_update: Optional[str] = Field(description="Last update date from the SFC page")

# ----------------- Licensing Conditions -----------------
class LicensingCondition(BaseModel):
    effective_date: Optional[date] = None
    condition_text: str


class IndividualConditions(BaseModel):
    ceref: str
    individual_name: str
    chinese_name: Optional[str] = None
    sfo_conditions: List[LicensingCondition] = []
    amlo_conditions: List[LicensingCondition] = []
    last_update: Optional[date] = None


# ----------------- Disciplinary Actions -----------------
class PressRelease(BaseModel):
    title: Optional[str] = None
    url: Optional[HttpUrl] = None


class DisciplinaryAction(BaseModel):
    date_of_action: Optional[date] = None
    action_taken: Optional[str] = None
    press_releases: List[PressRelease] = []


class IndividualDisciplinaryAction(BaseModel):
    ceref: str
    individual_name: str
    chinese_name: Optional[str] = None
    disciplinary_actions: List[DisciplinaryAction] = []
    last_update: Optional[date] = None


# ----------------- Licensee Record -----------------
class LicenseeRecord(BaseModel):
    address_type: Optional[str] = Field(None, description="Type of address (e.g., Principal, Business)")
    address: str = Field(..., description="Full postal address")
    effective_date: Optional[str] = Field(None, description="Effective date of this address")
    remarks: Optional[str] = Field(None, description="Additional notes or remarks")


class LicenseeRecordResponse(BaseModel):
    licensee_name: str
    cr_number: Optional[str]
    addresses: List[LicenseeRecord]


# ----------------- Individual Address -----------------
class AddressEntry(BaseModel):
    principal: str
    principal_code: Optional[str]
    address: str


class IndividualAddressesSchema(BaseModel):
    individual_name: Optional[str]
    individual_ceref: Optional[str]
    addresses: List[AddressEntry]
    last_updated: Optional[str]


# ----------------- Individual Licence -----------------
class RegulatedActivity(BaseModel):
    principal: str
    date_of_accreditation: Optional[str]
    regulated_activity: Optional[str]
    effective_date: Optional[str]
    licence_role: Optional[str]
    remarks: Optional[str]


class AMLORecord(BaseModel):
    principal: Optional[str]
    date_of_accreditation: Optional[str]
    virtual_asset_service: Optional[str]
    effective_date: Optional[str]
    licence_role: Optional[str]
    remarks: Optional[str]




#  Schemas for Corporation Role type

class LicenceRecord(BaseModel):
    """Schema for a single licence record of a corporation"""
    licence_type: str                          # e.g. "Advising on Securities"
    business_type: Optional[str] = None        # if available
    effective_date: Optional[date] = None      # e.g. "2004-04-01"
    licence_status: str                        # e.g. "Active"
    condition: Optional[str] = None            # any conditions applied


class CorporationLicenceSchema(BaseModel):
    """Schema for all licences of a corporation"""
    corp_name: str
    corp_ce_ref: str                           # Corporation CEREF ID, e.g. "AAB444"
    licences: List[LicenceRecord]

# Address

class CorporateAddress(BaseModel):
    type: str  # e.g., "Principal Place of Business", "Registered Office"
    address: str


class CorporateLicenceRecord(BaseModel):
    licence_number: str
    status: str  # e.g., Active, Revoked, Suspended
    regulated_activities: List[str]  # e.g., ["Type 1: Dealing in Securities"]
    effective_date: Optional[date]
    expiry_date: Optional[date]


class CorporateDetailSchema(BaseModel):
    corporation_name: str
    incorporation_date: Optional[date]
    business_registration_number: Optional[str]
    central_entity_number: Optional[str]  # CEREF
    company_type: Optional[str]  # e.g., Licensed Corporation, Registered Institution
    addresses: List[CorporateAddress] = []
    website: Optional[HttpUrl]

    licences: List[CorporateLicenceRecord] = []
    status: Optional[str]  # e.g., "Active", "Suspended", "Revoked"
    last_updated: Optional[date]


class BusinessAddress(BaseModel):
    address: str
    is_principal: bool = False  # Whether it's marked as "Principal place of business"

class CorporationBusinessAddress(BaseModel):
    corporation_name: str
    corporation_code: str
    business_addresses: List[BusinessAddress]
    website_address: Optional[HttpUrl]
    last_updated: Optional[date]