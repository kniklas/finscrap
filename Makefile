all: setup lint test clean

setup:
	@echo "Starting setup"
	python -m pip install --upgrade pip
	if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
	@echo "Completed setup"

lint:
	@echo "Starting lint"
	find . -name "*.yml" | xargs python -m yamllint
	find . -name "*.py" | xargs python -m black --check --verbose
	find . -name "*.py" | xargs python -m pylint
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
