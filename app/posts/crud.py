import boto3
from uuid import uuid4, UUID
from datetime import datetime, timezone
from fastapi import HTTPException
from app.posts.schema import CreatePostSchema, UpdatePostSchema


class PostsCrud:
    def __init__(self, table_name: str = "Posts", region_name: str = "eu-north-1"):
        self.dynamodb = boto3.resource("dynamodb", region_name=region_name)
        self.posts_table = self.dynamodb.Table(table_name)

    def create_post(self, data: CreatePostSchema):
        post_id = str(uuid4())
        now = datetime.now(timezone.utc).isoformat()
        item = {
            "id": post_id,
            "title": data.title,
            "body": data.body,
            "tags": data.tags,
            "createdDate": now,
            "updatedDate": now,
        }
        self.posts_table.put_item(Item=item)
        return item

    def get_posts(self):
        response = self.posts_table.scan()
        return response.get("Items", [])

    def get_post(self, post_id: UUID):
        response = self.posts_table.get_item(Key={"id": str(post_id)})
        item = response.get("Item")
        if not item:
            raise HTTPException(status_code=404, detail="Post not found")
        return item

    def update_post(self, post_id: UUID, data: UpdatePostSchema):
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No data provided for update")
        update_data["updatedDate"] = datetime.now(timezone.utc).isoformat()
        update_expression = "SET " + ", ".join(f"#{k}=:{k}" for k in update_data.keys())
        expression_values = {f":{k}": v for k, v in update_data.items()}
        expression_names = {f"#{k}": k for k in update_data.keys()}
        try:
            response = self.posts_table.update_item(
                Key={"id": str(post_id)},
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
            Key={"id": str(post_id)}, ReturnValues="ALL_OLD"
        )
        if "Attributes" not in response:
            raise HTTPException(status_code=404, detail="Post not found")
