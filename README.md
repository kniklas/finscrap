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

Review examples folder with docker lambda and dependencies implementation.

TODO: consider moving lambda example implementation and AWS infrastructure
deployment to separate repository.
