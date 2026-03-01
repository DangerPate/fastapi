from fastapi import FastAPI, Query, HTTPException
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session



SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/db" #"postgresql://postgres:postgres@postgresserver/db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

class Base(DeclarativeBase): pass

class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

tom = Person(name="Tom", age=38)
db.add(tom)
db.commit()
db.refresh(tom)

print(tom.id)

people = db.query(Person).all()
app = FastAPI()


''' computers = {
    "gaming": {
        'gpu': 'rtx3070',
        'cpu': 'i5-12400f',
        'ram': '32gb-ddr4-3200',
        'storage': 'nvme-ssd-1tb',
        'motherboard': 'b660m-a',
        'psu': '750w-80plus-gold',
        'cooling': 'tower-air-cooler',
        'case': 'mid-tower-atx'
    },
    "working": {
        'gpu': 'rtx-a2000',
        'cpu': 'i7-12700',
        'ram': '32gb-ddr4-3200-ecc',
        'storage': 'nvme-ssd-2tb',
        'motherboard': 'b660-pro',
        'psu': '650w-80plus-gold',
        'cooling': 'liquid-aio-240mm',
        'case': 'full-tower-quiet'
    },
    "home": {
        'gpu': 'uhd-graphics-730',
        'cpu': 'i3-12100',
        'ram': '16gb-ddr4-2666',
        'storage': 'sata-ssd-512gb',
        'motherboard': 'h610m-h',
        'psu': '450w-80plus-white',
        'cooling': 'stock-cooler',
        'case': 'micro-atx-slim'
    }
}
@app.get("/computer-type/{pc_type}")
async def computer_type(pc_type: str):
    if pc_type not in computers:
        raise HTTPException(status_code=404, detail="PC not found")
    return computers[pc_type]

class PCInfo(BaseModel):
    gpu: Optional[str] = None
    cpu: str
    ram: str
    storage: str
    motherboard: str
    psu: str
    cooling: str
    case: str

@app.post("/create-pc/{pc_type}")
async def create_pc(pc_type: str, new_pc: PCInfo):
    if pc_type in computers:
        return {'Error': 'Book already exists'}
    computers[pc_type] = new_pc
    return computers[pc_type]

class UpdatePC(BaseModel):
    gpu: Optional[str] = None
    cpu: Optional[str] = None
    ram: Optional[str] = None
    storage: Optional[str] = None
    motherboard: Optional[str] = None
    psu: Optional[str] = None
    cooling: Optional[str] = None
    case: Optional[str] = None

@app.put("/update-pc/{pc_type}")
async def update_pc(pc_type: str, upd_pc: UpdatePC):
    if pc_type not in computers:
        return {'Error': 'PC ID does not exists'}
    if upd_pc.gpu != None:
        computers[pc_type].gpu = upd_pc.gpu
    if upd_pc.cpu != None:
        computers[pc_type].cpu = upd_pc.cpu
    if upd_pc.ram != None:
        computers[pc_type].ram = upd_pc.ram
    if upd_pc.storage != None:
        computers[pc_type].storage = upd_pc.storage
    if upd_pc.motherboard != None:
        computers[pc_type].motherboard = upd_pc.motherboard
    if upd_pc.psu != None:
        computers[pc_type].psu = upd_pc.psu
    if upd_pc.cooling != None:
        computers[pc_type].cooling = upd_pc.cooling
    if upd_pc.case != None:
        computers[pc_type].case = upd_pc.case
    return computers[pc_type]

@app.delete('/delete-pc')
def delete_pc(pc_type: str = Query(..., description='Type PC')):
    if pc_type not in computers:
        return {'Error': 'PC ID does not exists'}
    del computers[pc_type]
    return {'Done': 'The PC successfully deleted'} '''