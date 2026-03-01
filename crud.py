from sqlalchemy.orm import Session
from models import Document
from schemas import DocumentCreate, DocumentUpdate


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
    db_doc.status = "active"
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc


def update_document(db: Session, doc_id: int, doc_update: DocumentUpdate):
    db_doc = get_document(db, doc_id)
    if db_doc is None:
        return None

    update_data = doc_update.model_dump(exclude_unset=True)
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
