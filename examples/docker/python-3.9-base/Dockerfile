FROM public.ecr.aws/lambda/python:3.9

# new.txt - dependencies identified by pip-compile
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# finscrap dependency from test.pypi.org
COPY requirements-test.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -i https://test.pypi.org/simple/ -r requirements-test.txt
