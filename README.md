# finscrap (WIP)

[![build](https://github.com/kniklas/finscrap/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/kniklas/finscrap/actions/workflows/build.yml)

[![Coverage Status](https://coveralls.io/repos/github/kniklas/finscrap/badge.svg?branch=main)](https://coveralls.io/github/kniklas/finscrap?branch=main)

Financial web scraping - Work In Progress

Objective of this project is to webscrap financial data and provide API
deployed in the cloud to access the data.


# How to use

Install the package (from test pypi):

`pip install --index-url https://test.pypi.org/simple/ finscrap`

Redirect output to csv file:

`python3 -m finscrap --csv output.csv funds.json`

Note: `--csv` option has shorter equivalent: `-c`

Redirect output to DynamoDB table called: _Table1_:

`python3 -m finscrap --dynamodb Table1 funds.json`

Note: `--dynamodb` option has shorter equivalent: `-d`. Make sure your runtime
environment has correct [AWS credentials
configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).

To get more help use: `python3 -m finscrap --help`

## Working with DynamoDB

When working on this project, you can look at `examples` folder to create
example DynamoDB table, put or get sample data.


# Contributing

## pre-commit

Run `pre-commit install` initially!

## Checking code locally

* `pre-commit run -a` - run pre-commit checks on all files
* `make test` - run unit tests and display coverage report
* `make e2e-csv` - run end to end tests with csv option
* `make` - run setup, lint, test and clean jobs

## Deploy lambda package

**Note**: move it later to CONTRIB.md or AWS examples documentation.

**Note**: set correct environment variable `AWS_ACCOUNT`, so other shell
scripts (incl. `Makefile`) can work with correct AWS account.

**Note**: make sure to configure correct AWS profile to have sufficient
permissions to operate on your AWS account.

Read very carefully these
[instructions](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html)

Steps:
1. Build python package using `make clean && make build`
1.1. Go to examples folder, create `package` folder
2. Build dependencies in package folder: `pip install --target ./package -r ../requirements-dev.txt`
2.0. Add finscap package: `pip install --target ./package
../dist/finscrap-0.0.dev8.tar.gz`
2.1. Add finscrap package to package folder: `pip install --target ./package -i https://test.pypi.org/simple/ finscrap==0.0.dev`
3. Zip dependencies using: `zip -r package pack.zip`
4. Add to zip lambda file, e.g.: `zip pack.zip lambda.py`
5. Create lambda function, note account number is replaced with XXXXXX: `aws lambda create-function --function-name get-data --zip-file fileb://pack.zip --runtime python3.9 --handler get-data.handler --role arn:aws:iam::XXXXXXXXXXXX:role/lambda-apigateway-role\`
6. Clean-up `./package` folder (TODO: add to `make clean`)
?: How to update lambda file and package from UI/CLI?
?. Build dependencies package using: `pip install --target ./package ../dist/finscrap-0.0.dev8.tar.gz`
