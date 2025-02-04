
from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    channel_title = Column(String, index=True)
    channel_username = Column(String, index=True)
    message_id = Column(Integer, unique=True, index=True)
    message = Column(String)
    message_date = Column(DateTime)
    media_path = Column(String, nullable=True)
    emoji_used = Column(String, nullable=True)
    youtube_links = Column(String, nullable=True)

