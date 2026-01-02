from pydantic import BaseModel

class PostCreate(BaseModel):
    title : str
    content : str

class ReturnResponse(BaseModel):
    title : str
    content : str