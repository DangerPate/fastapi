from sqlalchemy.orm import Session
from models import Document, DocumentStatus
from schemas import DocumentCreate, DocumentUpdate
from datetime import date, timedelta


def get_document(db: Session, doc_id: int):
    return db.query(Document).filter(Document.id == doc_id).first()


def get_document_by_number(db: Session, doc_number: str):
    return db.query(Document).filter(Document.document_number == doc_number).first()


def get_documents(db: Session, skip: int = 0, limit: int = 100, status: str = None):
    query = db.query(Document)
    if status:
        query = query.filter(Document.status == status)
    return query.offset(skip).limit(limit).all()


def create_document(db: Session, doc: DocumentCreate):
    db_doc = Document(**doc.model_dump())
    if db_doc.status == DocumentStatus.REVOKED.value:
        db_doc.revoked_at = date.today()
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc


def update_document(db: Session, doc_id: int, doc_update: DocumentUpdate):
    db_doc = get_document(db, doc_id)
    if db_doc is None:
        return None

    update_data = doc_update.model_dump(exclude_unset=True)

    if 'status' in update_data:
        new_status = update_data['status']
        old_status = db_doc.status
        if new_status == DocumentStatus.REVOKED.value and old_status != DocumentStatus.REVOKED.value:
            db_doc.revoked_at = date.today()
        elif new_status != DocumentStatus.REVOKED.value and old_status == DocumentStatus.REVOKED.value:
            db_doc.revoked_at = None

    for key, value in update_data.items():
        setattr(db_doc, key, value)

    db.commit()
    db.refresh(db_doc)
    return db_doc


def delete_document(db: Session, doc_id: int):
    db_doc = get_document(db, doc_id)
    if db_doc is None:
        return None
    db.delete(db_doc)
    db.commit()
    return db_doc

def auto_update_statuses(db: Session):
    today = date.today()

    docs_to_update = db.query(Document).filter(Document.status != DocumentStatus.REVOKED.value).all()
    for doc in docs_to_update:
        new_status = None
        if doc.valid_until < today:
            new_status = DocumentStatus.EXPIRED.value
        elif (doc.valid_until - today).days <= 7:
            new_status = DocumentStatus.EXPIRING_SOON.value
        else:
            new_status = DocumentStatus.ACTIVE.value

        if doc.status != new_status:
            doc.status = new_status

    week_ago = today - timedelta(days=7)
    docs_to_delete = db.query(Document).filter(
        Document.status == DocumentStatus.REVOKED.value,
        Document.revoked_at <= week_ago
    ).all()
    for doc in docs_to_delete:
        db.delete(doc)

    db.commit()
