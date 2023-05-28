from fastapi import FastAPI,HTTPException, Depends
from schemas import*
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()

app=FastAPI()

@app.get('/')
def read_api(db:Session=Depends(get_db)):
    return db.query(models.Books).all()

@app.get('/get_item/{book_id}/{book_title}')
def get_book(book_id:int,book_title:str,db:Session=Depends(get_db)):
    a=db.query(models.Books).filter(models.Books.id==book_id,models.Books.title==book_title).first()
    if a is None:
        return HTTPException(
            status_code=404,
            detail=f"ID {book_id} : Does not exists!"
        )
    return a 

@app.post("/")
def create_book(book:Book,db:Session=Depends(get_db)):
    book_model=models.Books()
    book_model.title=book.title
    book_model.author=book.author
    book_model.description=book.description
    book_model.rating=book.rating
    db.add(book_model)
    db.commit()
    return book

@app.put('/{book_id}')
def update_book(book_id:int,book:Book,db:Session=Depends(get_db)):
    book_model=db.query(models.Books).filter(models.Books.id==book_id).first()
    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {book_id} : Does not exists!"
        )
    for attr,value in book.dict().items():
        setattr(book_model,attr,value)
    db.add(book_model)
    db.commit()
    return book

@app.delete('/{book_id}')
def delete_book(book_id:int,db:Session=Depends(get_db)):
    book_model=db.query(models.Books).filter(models.Books.id==book_id).first()
    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {book_id} : Does not exists!"
        )
    db.query(models.Books).filter(models.Books.id==book_id).delete()
    db.commit()