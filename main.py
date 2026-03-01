from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database import engine, get_db, Base
from models import Document
from schemas import DocumentCreate, DocumentUpdate
import crud

# Создаём таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Реестр лицензий и сертификатов",
    description="CRUD API для управления лицензиями и сертификатами",
    version="1.0.1"
)

# ─────────────────────────────────────────────────────────────
# CREATE
# ─────────────────────────────────────────────────────────────
@app.post("/certificates/", status_code=status.HTTP_201_CREATED)
def create_certificate(cert: DocumentCreate, db: Session = Depends(get_db)):
    existing = crud.get_certificate_by_number(db, cert.cert_number)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Сертификат с таким номером уже существует"
        )
    return crud.create_certificate(db=db, cert=cert)

# ─────────────────────────────────────────────────────────────
# READ (All)
# ─────────────────────────────────────────────────────────────
@app.get("/certificates/")
def read_certificates(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[str] = Query(None, description="Фильтр по статусу: active, expired, revoked"),
    db: Session = Depends(get_db)
):
    crud.check_expired_certificates(db)
    return crud.get_certificates(db=db, skip=skip, limit=limit, status=status)

# ─────────────────────────────────────────────────────────────
# READ (One)
# ─────────────────────────────────────────────────────────────
@app.get("/certificates/{cert_id}")
def read_certificate(cert_id: int, db: Session = Depends(get_db)):
    cert = crud.get_certificate(db, cert_id=cert_id)
    if cert is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Сертификат не найден")
    return cert

# ─────────────────────────────────────────────────────────────
# UPDATE
# ─────────────────────────────────────────────────────────────
@app.put("/certificates/{cert_id}")
def update_certificate(cert_id: int, cert_update: DocumentUpdate, db: Session = Depends(get_db)):
    db_cert = crud.update_certificate(db=db, cert_id=cert_id, cert_update=cert_update)
    if db_cert is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Сертификат не найден")
    return db_cert

# ─────────────────────────────────────────────────────────────
# DELETE
# ─────────────────────────────────────────────────────────────
@app.delete("/certificates/{cert_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_certificate(cert_id: int, db: Session = Depends(get_db)):
    db_cert = crud.delete_certificate(db=db, cert_id=cert_id)
    if db_cert is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Сертификат не найден")
    return None