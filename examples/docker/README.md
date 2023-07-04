# Docker implementation of lambda

This is an example implementation of AWS Lambda with finscrap python package, so its execution could be orchestrated by AWS.

## Concept

Two docker containers are being built:
- `python-3.9-base` - includes python dependencies, including `finscrap` package from test PyPi server
- `python-3.9` - based on above image, adds only Python lambda code and funds configuration (NOTE: in the future, funds configuration should be taken as lambda parameter from S3 bucket) - see issue: #19

The latter image used when creation of the lambda function.

Concept is based on [AWS Lambda Python Docker Image instructions](https://docs.aws.amazon.com/lambda/latest/dg/python-image.html#python-image-instructions)

## Pre-requisites

Below conditions must be satisfied in order to correctly used docker images.

### Environment variables

They are required to correctly identify AWS account and AWS Region.
```shell
export AWS_DEFAULT_REGION=
export AWS_ACCOUNT=
```

Make sure that default AWS profile has correct permissions.

### AWS Resources

To work with AWS resources from command line, [AWS CLI must be installed](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

### DynamoDB table

Make sure the table(s) exist, see DynamoDB folder for examples how DynamoDB tables can be created and used from command line.

*Note*: index might need to be created to allow API Gateway access (**TBD**).

#### Lambda IAM Role

Correct IAM Role must be created for lambda function, so it can access other AWS resources.
See: [Tutorial: Using Lambda with API Gateway](https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway-tutorial.html#services-apigateway-tutorial-role)

To enable access of API Gateway to DynamoDB, add to `Trust relationships`, following:
```json
            "Sid": "Statement1",
            "Effect": "Allow",
            "Principal": {
                "Service": "apigateway.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
```

#### API Gateway

Created on base of [these guidelines](https://aws.amazon.com/blogs/compute/using-amazon-api-gateway-as-a-proxy-for-dynamodb/)
1. Create API (REST)
2.

#### ECR Repository

ECR repository is required to push, store and pull docker images:

```shell
# Create repository for base image:
aws ecr create-repository \
    --repository-name fin-scrap-base \
    --image-scanning-configuration scanOnPush=true \
    --image-tag-mutability MUTABLE
# Create repository for image with lambda executable
aws ecr create-repository \
    --repository-name fin-scrap
    --image-scanning-configuration scanOnPush=true \
    --image-tag-mutability MUTABLE
```

Before pushing, pulling images, make sure to authenticate with ECR:
```shell
aws ecr get-login-password \
    --region $AWS_DEFAULT_REGION | docker login --username AWS \
    --password-stdin $AWS_ACCOUNT.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com
```

### Resolved Python dependencies

Before image is build, make sure that python dependencies are solved and there are no conflicting versions of python packages.

```shell
pip-compile --extra-index-url=https://test.pypi.org/simple/ \
    --output-file=requirements.txt \
    requirements-test.txt ../../../requirements-build.txt
```

Note that `requirements-test.txt` includes only single package, it is a finscrap package on test PyPi server.

### Using Makefile

In order to use `Makefile` make sure you have correct executables on your operating system.


## Working with images

Make sure pre-requisites are satisfied.
Change contents of `version.txt` file in case dependencies, or anything else changes in the container.

### Automatic (via Makefile)

Execution of all commands in "Manual" section of this README.md is prone to error and time consuming, that's why repeatable activities are automated using `Makefile`.

Typically following activities are performed by the `Makefile`:
- authenticate to ECR
- build new image with tags based on version from lambda python file
- push new image to ECR
- update lambda with new image

### Manual

Base image instructions:

```shell
# Navigate to python-3.9-base folder
$ cd python-3.9-base
# Build base image
$ docker build -t python-3.9-base:test .
# Tag image as latest
$ docker tag python-3.9-base:test $AWS_ACCOUNT.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/fin-scrap-base:latest
# Tag image using version.txt
$ docker tag python-3.9-base:$(cat version.txt) \
    $AWS_ACCOUNT.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/fin-scrap-base:$(cat version.txt)
# Push image with all tags:
$ docker push $AWS_ACCOUNT.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/fin-scrap-base --all-tags
# Go back to previous folder
$ cd ..
```

Image with actual lambda executables:

```shell
# Navigate to python-3.9 folder
$ cd python-3.9
# Build lambda executable image
$ docker build -t python-3.9:test .
# Tag image as latest
$ docker tag python-3.9:test $AWS_ACCOUNT.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/fin-scrap:latest
# Tag image using version.txt
$ docker tag python-3.9:$(cat version.txt) \
    $AWS_ACCOUNT.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/fin-scrap:$(cat version.txt)
# Push image with all tags:
$ docker push $AWS_ACCOUNT.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/fin-scrap --all-tags
# Go back to previous folder
```

Create and update lambda:

```shell
# Create new lambda:
$ aws lambda create-function --function-name fin-scrap --package-type Image --code ImageUri=$AWS_ACCOUNT.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/fin-scrap:latest --role arn:aws:iam::$AWS_ACCOUNT:role/lambda-apigateway-role

# Upload changed lambda (image):
$ aws lambda update-function-code --function-name fin-scrap --image-uri $AWS_ACCOUNT.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/fin-scrap:latest
```

(Optional) Test locally image:

```shell
$ cd ..
# Test preparation: run docker image locally
$ docker run -p 9000:8080 \
    -v $HOME/.aws/credentials:/root/.aws/credentials:ro \
    -v $HOME/.aws/config:/root/.aws/config:ro \
    python-3.9:test
# In new console invoke lambda function:
$ curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d ''
# After testing is completed, kill docker process (replace XX with docker container ID)
$ docker ps
$ docker killl XX
```

For local testing, it is recommended to use:
- small configuration file with funds, to save time while waiting for results
- use test DynamoDB table (not production)
