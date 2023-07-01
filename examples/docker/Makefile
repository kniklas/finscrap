# Makefile to build docker images for finscrap Python package
# Author: Kamil Niklasiński (c) 2023

BASE_IMAGE_NAME=fin-scrap-base
BASE_REPO_NAME=fin-scrap-base
BASE_IMAGE_VERSION:= $(shell cat ${BASE_IMAGE_NAME}/version.txt)

LAMBDA_IMAGE_NAME=fin-scrap-lambda
LAMBDA_REPO_NAME=fin-scrap-lambda
LAMBDA_IMAGE_VERSION := $(shell cat ${LAMBDA_IMAGE_NAME}/version.txt)
LAMBDA_FUNCTION_NAME=fin-scrap

auth:
	aws ecr get-login-password \
		--region ${AWS_DEFAULT_REGION} | docker login --username AWS \
		--password-stdin ${AWS_ACCOUNT}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com

create-ecr-base:
	aws ecr create-repository \
		--repository-name ${BASE_REPO_NAME} \
		--image-scanning-configuration scanOnPush=true \
		--image-tag-mutability MUTABLE \
		--region ${AWS_DEFAULT_REGION}

create-ecr-lambda:
	aws ecr create-repository \
		--repository-name ${LAMBDA_REPO_NAME} \
		--image-scanning-configuration scanOnPush=true \
		--image-tag-mutability MUTABLE \
		--region ${AWS_DEFAULT_REGION}

build-base:
	cd ${BASE_IMAGE_NAME} && \
	docker build -t ${BASE_IMAGE_NAME}:test -t ${BASE_IMAGE_NAME}:${BASE_IMAGE_VERSION} .

build-lambda:
	cd ${LAMBDA_IMAGE_NAME} && \
	docker build -t ${LAMBDA_IMAGE_NAME}:test -t ${LAMBDA_IMAGE_NAME}:${LAMBDA_IMAGE_VERSION} .

build-all: build-base build-lambda

push-docker-base:
	cd ${BASE_IMAGE_NAME} && \
	docker tag ${BASE_IMAGE_NAME}:test \
		${AWS_ACCOUNT}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${BASE_REPO_NAME}:latest && \
	docker tag ${BASE_IMAGE_NAME}:${BASE_IMAGE_VERSION} \
		${AWS_ACCOUNT}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${BASE_REPO_NAME}:${BASE_IMAGE_VERSION} && \
	docker push ${AWS_ACCOUNT}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${BASE_REPO_NAME} --all-tags

push-docker-lambda:
	cd ${LAMBDA_IMAGE_NAME} && \
	docker tag ${LAMBDA_IMAGE_NAME}:test \
		${AWS_ACCOUNT}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${LAMBDA_REPO_NAME}:latest
	docker tag ${LAMBDA_IMAGE_NAME}:${LAMBDA_IMAGE_VERSION} \
		${AWS_ACCOUNT}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${LAMBDA_REPO_NAME}:${LAMBDA_IMAGE_VERSION}
	docker push ${AWS_ACCOUNT}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${LAMBDA_REPO_NAME} --all-tags

push-docker-all: push-docker-base push-docker-lambda

update-lambda:
	aws lambda update-function-code \
		--function-name ${LAMBDA_FUNCTION_NAME} \
		--image-uri ${AWS_ACCOUNT}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${LAMBDA_REPO_NAME}:latest

create-lambda:
	aws lambda create-function \
		--function-name ${LAMBDA_FUNCTION_NAME} \
		--package-type Image \
		--code ImageUri=${AWS_ACCOUNT}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${LAMBDA_REPO_NAME}:latest \
		--role arn:aws:iam::${AWS_ACCOUNT}:role/lambda-apigateway-role

# Use only if there are issues to refresh lambda docker image
remove:
	docker image rm ${LAMBDA_IMAGE_NAME}:test

run:
	aws lambda invoke --function-name ${LAMBDA_FUNCTION_NAME} response.json

all: auth build-all push-docker-all update-lambda

force-update: remove all

# First time setup
# Make sure that IAM role for lambda is created
setup: auth create-ecr-base create-ecr-lambda build-all push-docker-all create-lambda
