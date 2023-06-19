# Python 3.9 (fat) docker container

Link: https://docs.aws.amazon.com/lambda/latest/dg/python-image.html#python-image-instructions

Pros:
- easy to create
- easy for invocation and maintenance

Cons:
- size 2-3 bigger than slim (280M vs 770M)

# How to

Build image:
`docker build -t python-3.9:test`

## Run and test image locally

Run locally image:
```shell
docker run -p 9000:8080 \
    -v $HOME/.aws/credentials:/root/.aws/credentials:ro \
    -v $HOME/.aws/config:/root/.aws/config:ro \
    python-3.9:test
```

Test image (new console):
`curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'`

Kill running process:
`docker ps`
`docker killl XXXXXXX` - replacing X with process number


## Work with AWS ECR Repository

make sure correct environmet variables exist:
`export AWS_DEFAULT_REGION=`
`export AWS_ACCOUNT=`

Make sure IAM role is created.

## Use Makefie (recommended)

In most cases `make all` is sufficient to update lambda:
- authenticate to ECR
- build new image with tags based on version from lambda python file
- push new image to ECR
- update lambda with new image


## Manually via CLI

Authenticate docker with AWS ECR service
`aws ecr get-login-password --region ${AWS_DEFAULT_REGION}| docker login --username AWS --password-stdin ${AWS_ACCOUNT}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com`

Create ECR repository
`aws ecr create-repository --repository-name fin-scrap --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE`

Link local image name and tag with ECR repository
`docker tag python-3.9:test ${AWS_ACCOUNT}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/fin-scrap:latest`

Push image to ECR:
`docker push ${AWS_ACCOUNT}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/fin-scrap:latest`

Create new lambda:
`aws lambda create-function --function-name fin-scrap --package-type Image --code ImageUri=${AWS_ACCOUNT}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/fin-scrap:latest --role arn:aws:iam::${AWS_ACCOUNT}:role/lambda-apigateway-role`

Upload changed lambda (image):
`aws lambda update-function-code --function-name fin-scrap --image-uri ${AWS_ACCOUNT}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/fin-scrap:latest`
