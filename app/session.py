import boto3
from app.config import env_vars

session = boto3.Session(
    aws_access_key_id=env_vars.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=env_vars.AWS_SECRET_ACCESS_KEY,
    region_name=env_vars.REGION,
)
