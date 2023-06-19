"""Lambda function to webscrap and store data in DynamoDB"""

import os
import logging
from aws_xray_sdk.core import xray_recorder
from finscrap import finscrap


# pylint: disable=unused-argument
def lambda_handler(event, context):
    """Lambda handler"""

    lambda_version = "0.0.1"
    print("Lambda version: " + lambda_version)

    print("Enable logging")
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Display lambda function name and AWS execution environment
    lambda_function = os.environ.get("AWS_LAMBDA_FUNCTION_NAME")
    aws_execution_env = os.environ.get("AWS_EXECUTION_ENV")
    print("Lambda function: " + lambda_function)
    print("AWS execution environment: " + aws_execution_env)

    funds_json = "funds_prv.json"
    dynamo_db = "Assets1"

    # start subsegment
    # pylint: disable=unused-variable
    subsegment = xray_recorder.begin_subsegment("webscrap")

    # code to be instrumented
    webscrap = finscrap.AssetsWrapper(funds_json)
    webscrap.get_data()
    webscrap.out_dynamodb(dynamo_db)

    # NOTE: below code for illustratino/example only
    subsegment.put_metadata("key", dict, "namespace")
    subsegment.put_annotation("key", "value")

    # stop subsegment
    xray_recorder.end_subsegment()
    return {"statusCode": 200}
