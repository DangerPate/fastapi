from sqlalchemy import Column, Integer, String, Date, Enum, Boolean
from database import Base
import enum

class DocumentType(str, enum.Enum):
    LICENSE = "licence"
    SRO_CERTIFICATE = "sro certificate"
    ACCREDITATION = "accreditation"
    ISO_CERTIFICATE = "iso_certificate"
    FSTEC_LICENSE = "fstec_license"

class DocumentStatus(str, enum.Enum):
    ACTIVE = "active"
    EXPIRING_SOON = "expiring_soon"
    EXPIRED = "expired"
    SUSPENDED = "suspended"
    REVOKED = "revoked"
    ARCHIVED = "archived"

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    document_number = Column(String(50), unique=True, index=True, nullable=False)
    document_name = Column(String(200), nullable=False)
    document_type = Column(Enum(*[x.value for x in DocumentType], name="document_type"), nullable=False)
    issuer = Column(String(200), nullable=False)
    issue_date = Column(Date, nullable=False)
    valid_from = Column(Date, nullable=False)
    valid_until = Column(Date, nullable=False)
    status = Column(Enum(*[x.value for x in DocumentStatus], name="document_status"), default="active", nullable=False)
    holder_name = Column(String(200), nullable=False)
    is_indefinite = Column(Boolean, default=False, nullable=False)
    description = Column(String(200), nullable=True)