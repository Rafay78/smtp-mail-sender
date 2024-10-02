from pydantic import BaseModel, HttpUrl

class User(BaseModel):
    name: str
    email: str
    picture: HttpUrl 

class TokenRequest(BaseModel):
    token: str


class TokenRequest(BaseModel):
    code: str