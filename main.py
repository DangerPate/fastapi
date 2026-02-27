from fastapi import FastAPI, Query, HTTPException
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


bookshelf = {
       1: {
           'book': 'Ulyss',
           'price': 4.75,
           'author': 'James Joyce'
       },

       2: {
           'book': 'Three Men in a Boat (To Say Nothing of the Dog)',
           'price': 3.99,
           'author': 'Jerome K. Jerome'
       }
   }

@app.get("/get-book/{book_id}")
async def get_book(book_id: int):
    if book_id not in bookshelf:
        raise HTTPException(status_code=404, detail="Book not found")
    return bookshelf[book_id]

class BookInfo(BaseModel):
    book: str
    price: float
    author: Optional[str] = None


@app.post("/create-book/{book_id}")
async def create_book(book_id: int, new_book: BookInfo):
    if book_id in bookshelf:
        return {'Error': 'Book already exists'}
    bookshelf[book_id] = new_book
    return bookshelf[book_id]

class UpdateBook(BaseModel):
    book: Optional[str] = None
    price: Optional[float] = None
    author: Optional[str] = None

@app.put('/update-book/{book_id}')
async def update_book(book_id: int, upd_book: UpdateBook):
    if book_id not in bookshelf:
        return {'Error': 'Book ID does not exists'}
    if upd_book.book != None:
        bookshelf[book_id].book = upd_book.book
    if upd_book.price != None:
        bookshelf[book_id].price = upd_book.price
    if upd_book.author != None:
        bookshelf[book_id].author = upd_book.author
    return bookshelf[book_id]

book_id: int = Query(..., description='The book ID must be greater than zero')

@app.delete('/delete-book')
def delete_book(book_id: int = Query(..., description='The book ID must be greater than zero')):
    if book_id not in bookshelf:
        return {'Error': 'Book ID does not exists'}
    del bookshelf[book_id]
    return {'Done': 'The book successfully deleted'}


computers = {
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
    return {'Done': 'The PC successfully deleted'}