from fastapi import FastAPI
from database import engine, SessionLocal
import models, crud
from schemas import MessageCreate, MessageResponse
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/messages/", response_model=MessageResponse)
def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    return crud.create_message(db, message)

@app.get("/messages/{message_id}", response_model=MessageResponse)
def read_message(message_id: int, db: Session = Depends(get_db)):
    return crud.get_message(db, message_id)

@app.get("/messages/", response_model=list[MessageResponse])
def list_messages(db: Session = Depends(get_db)):
    return crud.get_messages(db)

@app.delete("/messages/{message_id}", response_model=MessageResponse)
def delete_message(message_id: int, db: Session = Depends(get_db)):
    return crud.delete_message(db, message_id)
