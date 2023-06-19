IMAGE_NAME=python-3.9
REPO_NAME=fin-scrap
IMAGE_VERSION := $(shell cat version.txt)

auth:
	aws ecr get-login-password \
		--region ${AWS_DEFAULT_REGION} | docker login --username AWS \
		--password-stdin ${AWS_ACCOUNT}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com

build:
	docker build -t ${IMAGE_NAME}:test -t ${IMAGE_NAME}:${IMAGE_VERSION} .

push:
	# Add version and latest tags
	docker tag ${IMAGE_NAME}:test ${AWS_ACCOUNT}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${REPO_NAME}:latest
	docker tag ${IMAGE_NAME}:${IMAGE_VERSION} ${AWS_ACCOUNT}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${REPO_NAME}:${IMAGE_VERSION}
	# Push image to ECR
	docker push ${AWS_ACCOUNT}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${REPO_NAME} --all-tags

update-lambda:
	aws lambda update-function-code \
		--function-name ${REPO_NAME} \
		--image-uri ${AWS_ACCOUNT}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${REPO_NAME}:latest

remove:
	docker image rm ${IMAGE_NAME}:test

create-lambda:
	aws lambda create-function \
		--function-name ${REPO_NAME} \
		--package-type Image \
		--code ImageUri=${AWS_ACCOUNT}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${REPO_NAME}:latest \
		--role arn:aws:iam::${AWS_ACCOUNT}:role/lambda-apigateway-role

create-ecr:
	aws ecr create-repository \
		--repository-name ${REPO_NAME} \
		--image-scanning-configuration scanOnPush=true \
		--image-tag-mutability MUTABLE \
		--region ${AWS_DEFAULT_REGION}

run:
	aws lambda invoke --function-name ${REPO_NAME} response.json

# Typical scenario
all: auth build push update-lambda

# Use if docker images are not updated
force-update: remove all

# Use when new setup must be create
# NOTE: IAM Lambda role (lambda-apigateway) must be created before!
setup: build auth create-ecr push create-lambda
