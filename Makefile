include .env

.EXPORT_ALL_VARIABLES:
APP_NAME=aws-fastapi-project

TAG=latest
TF_VAR_app_name=${APP_NAME}
REGISTRY_NAME=${APP_NAME}
TF_VAR_image=${AWS_ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REGISTRY_NAME}:${TAG}
TF_VAR_region=${REGION}
TF_VAR_aws_access_key_id=${AWS_ACCESS_KEY_ID}
TF_VAR_aws_secret_access_key=${AWS_SECRET_ACCESS_KEY}
TF_VAR_jwt_secret=${JWT_SECRET}
TF_VAR_client_id=${CLIENT_ID}
TF_VAR_client_secret=${CLIENT_SECRET}
TF_VAR_table_name=${TABLE_NAME}


setup-ecr:
	cd infra/setup && terraform init && terraform apply -auto-approve

deploy-container:
	sh deploy.sh

deploy-accessories:
	sh deploy-accessories.sh

deploy-service:
	cd infra/app && terraform init && terraform apply -auto-approve

destroy-service:
	cd infra/app && terraform init && terraform destroy -auto-approve

destroy-accessories:
	sam delete --stack-name AwsFastapiProjectAccessories