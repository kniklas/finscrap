# Docker building steps

## Pre-conditions

- Make sure correct environmet variables exist:
`export AWS_DEFAULT_REGION=`
`export AWS_ACCOUNT=`

- ECR repository exists `fin-scrap-base` in correct region.
```shell
aws ecr create-repository \
    --repository-name fin-scrap-base \
    --image-scanning-configuration scanOnPush=true \
    --image-tag-mutability MUTABLE
```

- Python dependencies are resolved:
```shell
pip-compile --extra-index-url=https://test.pypi.org/simple/ \
    --output-file=requirements.txt \
    requirements-test.txt ../../../requirements-build.txt
```

## Building process

Build image:
`docker build -t python-3.9-base:test .`

If necessary tag image to destination repository:
`docker tag python-3.9-base:test $AWS_ACCOUNT.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/fin-scrap-base:latest`

Push image:
`docker push $AWS_ACCOUNT.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/fin-scrap-base:latest`

Make sure that Dockerfile which is using this base image has correct URI.
