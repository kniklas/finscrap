all: setup lint test clean

setup:
	@echo "Starting build setup"
	python -m pip install --upgrade pip
	if [ -f requirements-build.txt ]; \
		then pip install -r requirements-build.txt; fi
	@echo "Completed setup"

setup-dev:
	@echo "Starting setup dev envirnoment"
	python -m pip install --upgrade pip
	if [ -f requirements-dev.txt ]; then pip install -r requirements-dev.txt; fi
	@echo "Completed setup of dev environment"

lint:
	@echo "Starting lint"
	find . -name "*.yml" -o -name "*.yaml" | xargs python -m yamllint
	find . -name "*.py" -not -path "./build/*" \
		| xargs python -m black -l 79 --check --verbose
	find . -name "*.py" -not -path "./build/*" \
		| xargs python -m pylint
	@echo "Completed lint"

test:
	@echo "Starting tests"
	coverage run -m --source=src/ -m pytest
	coverage report -m
	@echo "Completed tests"

build: clean
	@echo BUILDING PACKAGE
	python3 -m pip install --upgrade setuptools wheel
	python3 setup.py sdist bdist_wheel
	pip install -e .

pypi-test: build
	twine upload -r testpypi --config-file ~/.finpypirc --skip-existing ./dist/*

clean:
	@echo "Starting clean"
	rm -rvf dist build  .pytest_cache
	find . -type d -name __pycache__ -exec rm -r {} \+
	find . -type d -name finscrap.egg-info -exec rm -r {} \+
	@echo "Completed clean"

help:
	python -m finscrap --help

e2e:
	python -m finscrap tests/funds.json

e2e-csv:
	python -m finscrap -c out.csv tests/funds-short.json
	cat out.csv

# use Asssets2 table for testing of DynamoDB
e2e-dynamo:
	python -m finscrap -d Assets2 tests/funds-short.json
