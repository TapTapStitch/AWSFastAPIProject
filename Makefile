include .env

.EXPORT_ALL_VARIABLES:
APP_NAME=aws-fastapi-project

TAG=latest
TF_VAR_app_name=${APP_NAME}
REGISTRY_NAME=${APP_NAME}
TF_VAR_image=${AWS_ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REGISTRY_NAME}:${TAG}
TF_VAR_region=${REGION}


setup-ecr:
	cd infra/setup && terraform init && terraform apply -auto-approve

deploy-container:
	sh deploy.sh

deploy-service:
	cd infra/app && terraform init && terraform apply -auto-approve

destroy-service:
	cd infra/app && terraform init && terraform destroy -auto-approve