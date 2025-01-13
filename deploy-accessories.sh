#!/bin/bash

PROJECT_NAME="AwsFastapiProjectAccessories"

sam deploy \
    --template-file template.yaml \
    --resolve-s3 \
    --stack-name "$PROJECT_NAME" \
    --capabilities CAPABILITY_NAMED_IAM


echo "Accessories deployed successfully"