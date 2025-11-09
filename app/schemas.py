from pydantic import BaseModel
from typing import Union
import datetime as dt

class ToolCallFunction(BaseModel):
    name: str
    arguments: Union[str, dict]

class ToolCall(BaseModel):
    id: str
    function: ToolCallFunction

class Message(BaseModel):
    toolCalls: list[ToolCall]

class VapiRequest(BaseModel):
    message: Message

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Union[str, None]
    completed: bool

    class Config:
        from_attributes = True

class ReminderResponse(BaseModel):
    id: int
    reminder_text: str
    importance: str

    class Config:
        from_attributes = True

class CalendarEventResponse(BaseModel):
    id: int
    title: str
    description: Union[str, None]
    event_from: dt.datetime
    event_to: dt.datetime

    class Config:
        from_attributes = True
