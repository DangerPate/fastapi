import os
from fastapi import FastAPI, Depends, HTTPException, Query, status, APIRouter
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from database import engine, get_db, Base, SessionLocal
from schemas import DocumentCreate, DocumentUpdate
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import crud
import atexit

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Реестр лицензий и сертификатов",)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api")

@api_router.post("/documents/", status_code=status.HTTP_201_CREATED)
def create_document(doc: DocumentCreate, db: Session = Depends(get_db)):
    existing = crud.get_document_by_number(db, doc.document_number)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Документ с таким номером уже существует"
        )
    return crud.create_document(db=db, doc=doc)

@api_router.get("/documents/")
def read_documents(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[str] = Query(None, description="Фильтр по статусу: active, expired, revoked"),
    db: Session = Depends(get_db)
):
    return crud.get_documents(db=db, skip=skip, limit=limit, status=status)

@api_router.get("/documents/{doc_id}")
def read_document(doc_id: int, db: Session = Depends(get_db)):
    doc = crud.get_document(db, doc_id=doc_id)
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Документ не найден")
    return doc

@api_router.put("/documents/{doc_id}")
def update_document(doc_id: int, doc_update: DocumentUpdate, db: Session = Depends(get_db)):
    db_doc = crud.update_document(db=db, doc_id=doc_id, doc_update=doc_update)
    if db_doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Документ не найден")
    return db_doc

@api_router.delete("/documents/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    db_doc = crud.delete_document(db=db, doc_id=doc_id)
    if db_doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Документ не найден")
    return None

app.include_router(api_router)

frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")
else:
    print("Frontend dist not found. Run 'npm run build' in frontend folder.")

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

def scheduled_task():
    db = SessionLocal()
    try:
        crud.auto_update_statuses(db)
    finally:
        db.close()

scheduler = BackgroundScheduler()
scheduler.add_job(
    func=scheduled_task,
    trigger=IntervalTrigger(hours=24),
    id='auto_update_document_statuses',
    replace_existing=True
)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

@app.post("/admin/run-status-update", status_code=status.HTTP_200_OK)
def run_status_update(db: Session = Depends(get_db)):
    crud.auto_update_statuses(db)
    return {"message": "Status update completed"}