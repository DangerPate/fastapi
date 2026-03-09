from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
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
    document_number: str = Field(..., min_length=3, max_length=50)
    document_name: str = Field(..., min_length=3, max_length=200)
    document_type: DocumentType
    issuer: str = Field(..., min_length=3, max_length=200)
    issue_date: date
    valid_from: date
    valid_until: date
    status: DocumentStatus
    holder_name: str = Field(..., min_length=3, max_length=200)
    is_indefinite: bool
    description: Optional[str] = Field(default=None, max_length=200)

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(BaseModel):
    document_number: Optional[str] = Field(None, min_length=3, max_length=50)
    document_name: Optional[str] = Field(None, min_length=3, max_length=200)
    document_type: Optional[DocumentType] = None
    issuer: Optional[str] = Field(None, min_length=3, max_length=200)
    issue_date: Optional[date] = None
    valid_from: Optional[date] = None
    valid_until: Optional[date] = None
    status: Optional[DocumentStatus] = None
    revoked_at: Optional[date] = None
    holder_name: Optional[str] = Field(None, min_length=3, max_length=200)
    is_indefinite: Optional[bool] = None
    description: Optional[str] = Field(default=None, max_length=200)
