from pydantic import BaseModel


class SignUp(BaseModel):
    username: str
    password: str
    email: str


class ConfirmAccount(BaseModel):
    username: str
    confirmation_code: str


class SignIn(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
