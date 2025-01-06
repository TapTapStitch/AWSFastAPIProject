import boto3
from uuid import uuid4, UUID
from datetime import datetime, timezone
from fastapi import HTTPException
from .schema import CreatePostSchema, UpdatePostSchema


class PostsCrud:

    def __init__(self, table_name: str = "Posts"):
        self.dynamodb = boto3.resource("dynamodb")
        self.posts_table = self.dynamodb.Table(table_name)

    def create_post(self, data: CreatePostSchema):
        post_id = str(uuid4())
        now = datetime.now(timezone.utc).isoformat()
        item = {
            "id": post_id,
            "title": data["title"],
            "body": data["body"],
            "tags": data.get("tags", []),
            "createdDate": now,
            "updatedDate": now,
        }
        self.posts_table.put_item(Item=item)
        return item

    def get_posts(self):
        response = self.posts_table.scan()
        return response.get("Items", [])

    def get_post(self, post_id: UUID):
        response = self.posts_table.get_item(Key={"id": post_id})
        if "Item" not in response:
            raise HTTPException(status_code=404, detail="Post not found")
        return response["Item"]

    def update_post(self, post_id: UUID, data: UpdatePostSchema):
        now = datetime.now(timezone.utc).isoformat()
        update_expression = "SET "
        expression_values = {}
        expression_names = {}

        for key, value in data.items():
            if value is not None:
                expression_names[f"#{key}"] = key
                expression_values[f":{key}"] = value
                update_expression += f"#{key} = :{key}, "

        update_expression += "#updatedDate = :updatedDate"
        expression_names["#updatedDate"] = "updatedDate"
        expression_values[":updatedDate"] = now

        try:
            response = self.posts_table.update_item(
                Key={"id": post_id},
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_names,
                ExpressionAttributeValues=expression_values,
                ReturnValues="ALL_NEW",
            )
        except self.posts_table.meta.client.exceptions.ConditionalCheckFailedException:
            raise HTTPException(status_code=404, detail="Post not found")
        return response["Attributes"]

    def delete_post(self, post_id: UUID):
        response = self.posts_table.delete_item(
            Key={"id": post_id}, ReturnValues="ALL_OLD"
        )
        if "Attributes" not in response:
            raise HTTPException(status_code=404, detail="Post not found")
