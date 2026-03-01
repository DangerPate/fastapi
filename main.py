from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from database import engine, get_db, Base
from schemas import DocumentCreate, DocumentUpdate
import crud

# Создаём таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Реестр лицензий и сертификатов",
)

@app.post("/documents/", status_code=status.HTTP_201_CREATED)
def create_document(doc: DocumentCreate, db: Session = Depends(get_db)):
    existing = crud.get_document_by_number(db, doc.document_number)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Документ с таким номером уже существует"
        )
    return crud.create_document(db=db, doc=doc)

@app.get("/documents/")
def read_documents(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[str] = Query(None, description="Фильтр по статусу: active, expired, revoked"),
    db: Session = Depends(get_db)
):
    return crud.get_documents(db=db, skip=skip, limit=limit, status=status)

@app.get("/documents/{doc_id}")
def read_document(doc_id: int, db: Session = Depends(get_db)):
    doc = crud.get_document(db, doc_id=doc_id)
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Документ не найден")
    return doc

@app.put("/documents/{doc_id}")
def update_document(doc_id: int, doc_update: DocumentUpdate, db: Session = Depends(get_db)):
    db_doc = crud.update_document(db=db, doc_id=doc_id, doc_update=doc_update)
    if db_doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Документ не найден")
    return db_doc

@app.delete("/documents/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    db_doc = crud.delete_document(db=db, doc_id=doc_id)
    if db_doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Документ не найден")
    return None