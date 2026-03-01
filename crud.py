from sqlalchemy.orm import Session
from models import Document
from schemas import DocumentCreate, DocumentUpdate
from datetime import date


def get_certificate(db: Session, cert_id: int):
    return db.query(Document).filter(Document.id == cert_id).first()


def get_certificate_by_number(db: Session, cert_number: str):
    return db.query(Document).filter(Document.cert_number == cert_number).first()


def get_certificates(db: Session, skip: int = 0, limit: int = 100, status: str = None):
    query = db.query(Document)
    if status:
        query = query.filter(Document.status == status)
    return query.offset(skip).limit(limit).all()


def create_certificate(db: Session, cert: DocumentCreate):
    db_cert = Document(**cert.model_dump())
    db_cert.status = "active"
    db.add(db_cert)
    db.commit()
    db.refresh(db_cert)
    return db_cert


def update_certificate(db: Session, cert_id: int, cert_update: DocumentUpdate):
    db_cert = get_certificate(db, cert_id)
    if db_cert is None:
        return None

    update_data = cert_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_cert, key, value)

    db.commit()
    db.refresh(db_cert)
    return db_cert


def delete_certificate(db: Session, cert_id: int):
    db_cert = get_certificate(db, cert_id)
    if db_cert is None:
        return None
    db.delete(db_cert)
    db.commit()
    return db_cert


def check_expired_certificates(db: Session):
    today = date.today()
    expired = db.query(Document).filter(
        Document.expiry_date < today,
        Document.status == "active"
    ).all()
    for cert in expired:
        cert.status = "expired"
    db.commit()
    return expired