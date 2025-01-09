from fastapi import APIRouter, HTTPException, Depends, Response
from app.auth.schema import SignUp, ConfirmAccount, SignIn, Token
from app.auth.service import calculate_secret_hash, create_jwt_token, cognito_client
from app.config import env_vars

router = APIRouter()


@router.post(
    "/signup",
    status_code=201,
    responses={
        "400": {
            "description": "Bad request",
            "content": {
                "application/json": {
                    "examples": {
                        "username_exists": {
                            "summary": "Username already exists",
                            "value": {"detail": "Username already exists"},
                        }
                    }
                }
            },
        },
    },
)
def signup(user: SignUp = Depends(SignUp.as_form)):
    try:
        cognito_client.sign_up(
            ClientId=env_vars.CLIENT_ID,
            SecretHash=calculate_secret_hash(user.username),
            Username=user.username,
            Password=user.password,
            UserAttributes=[
                {"Name": "email", "Value": user.email},
            ],
        )
        return Response(status_code=201)
    except cognito_client.exceptions.UsernameExistsException:
        raise HTTPException(status_code=400, detail="Username already exists")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/confirm",
    status_code=200,
    responses={
        "400": {
            "description": "Bad request",
            "content": {
                "application/json": {
                    "examples": {
                        "invalid_code": {
                            "summary": "Invalid confirmation code",
                            "value": {"detail": "Invalid confirmation code"},
                        }
                    }
                }
            },
        },
    },
)
def confirm(user: ConfirmAccount = Depends(ConfirmAccount.as_form)):
    try:
        cognito_client.confirm_sign_up(
            ClientId=env_vars.CLIENT_ID,
            SecretHash=calculate_secret_hash(user.username),
            Username=user.username,
            ConfirmationCode=user.confirmation_code,
        )
        return Response(status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/signin",
    response_model=Token,
    status_code=200,
    responses={
        "401": {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "examples": {
                        "invalid_credentials": {
                            "summary": "Invalid username or password",
                            "value": {"detail": "Invalid username or password"},
                        }
                    }
                }
            },
        },
        "400": {
            "description": "Bad request",
            "content": {
                "application/json": {
                    "examples": {
                        "server_error": {
                            "summary": "Server encountered an error",
                            "value": {"detail": "Server encountered an error"},
                        }
                    }
                }
            },
        },
    },
)
def signin(user: SignIn = Depends(SignIn.as_form)):
    try:
        cognito_client.initiate_auth(
            ClientId=env_vars.CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": user.username,
                "PASSWORD": user.password,
                "SECRET_HASH": calculate_secret_hash(user.username),
            },
        )
        token = create_jwt_token(user.username)
        return {"access_token": token, "token_type": "bearer"}
    except cognito_client.exceptions.NotAuthorizedException as e:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
