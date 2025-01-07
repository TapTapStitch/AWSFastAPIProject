import pytest
import boto3
from moto import mock_aws
from fastapi.testclient import TestClient
from app.posts.crud import PostsCrud
from app.main import app
from app.posts.router import get_posts_crud


@pytest.fixture
def dynamodb():
    with mock_aws():
        dynamodb = boto3.resource("dynamodb", region_name="eu-north-1")
        table = dynamodb.create_table(
            TableName="Posts",
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        table.meta.client.get_waiter("table_exists").wait(TableName="Posts")
        yield dynamodb


@pytest.fixture(scope="function")
def posts_crud(dynamodb):
    return PostsCrud(table_name="Posts", region_name="eu-north-1")


@pytest.fixture(scope="function")
def client(posts_crud):
    app.dependency_overrides[get_posts_crud] = lambda: posts_crud
    client = TestClient(app)
    yield client
    app.dependency_overrides.pop(get_posts_crud)
