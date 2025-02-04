from sqlalchemy.orm import Session
import models, schemas

def create_message(db: Session, message: schemas.MessageCreate):
    db_message = models.Message(**message.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_message(db: Session, message_id: int):
    return db.query(models.Message).filter(models.Message.message_id == message_id).first()

def get_messages(db: Session):
    return db.query(models.Message).all()

def delete_message(db: Session, message_id: int):
    message = db.query(models.Message).filter(models.Message.message_id == message_id).first()
    if message:
        db.delete(message)
        db.commit()
    return message
