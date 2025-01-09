from fastapi import Form
from pydantic import BaseModel


class SignUp(BaseModel):
    username: str
    password: str
    email: str

    @classmethod
    def as_form(
        cls,
        username: str = Form(...),
        password: str = Form(...),
        email: str = Form(...),
    ):
        return cls(username=username, password=password, email=email)


class ConfirmAccount(BaseModel):
    username: str
    confirmation_code: str

    @classmethod
    def as_form(
        cls,
        username: str = Form(...),
        confirmation_code: str = Form(...),
    ):
        return cls(username=username, confirmation_code=confirmation_code)


class SignIn(BaseModel):
    username: str
    password: str

    @classmethod
    def as_form(
        cls,
        username: str = Form(...),
        password: str = Form(...),
    ):
        return cls(username=username, password=password)


class Token(BaseModel):
    access_token: str
    token_type: str
