#!/bin/bash

DEPLOY_DIR="deploy"
PROJECT_NAME="testproject"

mkdir -p "$DEPLOY_DIR/fastapi/app"

cp app/main.py "$DEPLOY_DIR/fastapi/"
touch "$DEPLOY_DIR/fastapi/__init__.py"

rsync -av --exclude='main.py' app/ "$DEPLOY_DIR/fastapi/app/"

pip install -r "requirements.txt" --target "$DEPLOY_DIR/lambda_layer/python/lib/python3.13/site-packages" --only-binary=:all: --platform manylinux2014_x86_64

sam deploy \
    --template-file template.yaml \
    --resolve-s3 \
    --stack-name "$PROJECT_NAME" \
    --capabilities CAPABILITY_NAMED_IAM

rm -r "$DEPLOY_DIR"