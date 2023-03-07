# finscrap (WIP)

[![build](https://github.com/kniklas/finscrap/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/kniklas/finscrap/actions/workflows/build.yml)

[![Coverage Status](https://coveralls.io/repos/github/kniklas/finscrap/badge.svg?branch=main)](https://coveralls.io/github/kniklas/finscrap?branch=main)

Financial web scraping - Work In Progress

Objective of this project is to webscrap financial data and provide API
deployed in the cloud to access the data.


# How to use

Install the package (from test pypi):

`pip install --index-url https://test.pypi.org/simple/ finscrap`

Run webscraping with output to STDOUT using definition in `funds.json` file::

`python3 -m finscrap funds.json`

Redirect output to csv file:

`python3 -m finscrap > funds.csv`


# Contributing

## pre-commit

Run `pre-commit install` initially!

## Checking code locally

* `pre-commit run -a` - run pre-commit checks on all files
* `make test` - run unit tests and display coverage report
* `make` - run setup, lint, test and clean jobs
