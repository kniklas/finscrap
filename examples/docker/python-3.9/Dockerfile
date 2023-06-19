# Use base image with python dependencies
FROM 638061828812.dkr.ecr.eu-west-2.amazonaws.com/fin-scrap-base:0.0.1

# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Copy json test file
COPY funds_prv.json ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.lambda_handler" ]
