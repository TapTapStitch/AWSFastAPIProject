from app.auth.schema import SignUp, ConfirmAccount, SignIn, Token


def test_signup_creation():
    data = {"username": "testuser", "password": "testpass", "email": "test@example.com"}
    user = SignUp(**data)
    assert user.username == "testuser"
    assert user.password == "testpass"
    assert user.email == "test@example.com"


def test_confirm_account_creation():
    data = {"username": "testuser", "confirmation_code": "123456"}
    account = ConfirmAccount(**data)
    assert account.username == "testuser"
    assert account.confirmation_code == "123456"


def test_signin_creation():
    data = {"username": "testuser", "password": "testpass"}
    signin = SignIn(**data)
    assert signin.username == "testuser"
    assert signin.password == "testpass"


def test_token_creation():
    data = {"access_token": "fake_token", "token_type": "bearer"}
    token = Token(**data)
    assert token.access_token == "fake_token"
    assert token.token_type == "bearer"
