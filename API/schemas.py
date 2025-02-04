from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):
    channel_title: str
    channel_username: str
    message_id: int
    message: str
    message_date: datetime
    media_path: str | None = None
    emoji_used: str | None = None
    youtube_links: str | None = None

class MessageResponse(MessageCreate):
    id: int

    class Config:
        from_attributes = True

