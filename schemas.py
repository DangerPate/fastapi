from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from enum import Enum

class DocumentType(str, Enum):
    LICENSE = "licence"
    SRO_CERTIFICATE = "sro certificate"
    ACCREDITATION = "accreditation"
    ISO_CERTIFICATE = "iso_certificate"
    FSTEC_LICENSE = "fstec_license"

class DocumentStatus(str, Enum):
    ACTIVE = "active"
    EXPIRING_SOON = "expiring_soon"
    EXPIRED = "expired"
    SUSPENDED = "suspended"
    REVOKED = "revoked"
    ARCHIVED = "archived"
class DocumentBase(BaseModel):
    document_type: DocumentType
    status: DocumentStatus
    document_number: str = Field(..., min_length=3, max_length=50)
    document_name: str = Field(..., min_length=3, max_length=200)
    issuer: str = Field(..., min_length=3, max_length=200)
    issue_date: date
    valid_from: date
    valid_until: date
    holder_name: str = Field(..., min_length=3, max_length=200)
    is_indefinite: bool
    description: Optional[str] = Field(None, min_length=3, max_length=200)

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(BaseModel):
    document_type: DocumentType
    status: DocumentStatus
    document_number: str = Field(..., min_length=3, max_length=50)
    document_name: str = Field(..., min_length=3, max_length=200)
    issuer: str = Field(..., min_length=3, max_length=200)
    issue_date: date
    valid_from: date
    valid_until: date
    holder_name: str = Field(..., min_length=3, max_length=200)
    is_indefinite: bool
    description: Optional[str] = Field(None, min_length=3, max_length=200)
