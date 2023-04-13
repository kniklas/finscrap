# pylint: disable=invalid-name
"""Example lambda function"""

from finscrap import finscrap


# pylint: disable=unused-argument
def lambda_handler(event, context):
    """Lambda handler"""

    FUNDS_JSON = "funds-short.json"
    DYNAMO_DB = "Assets2"

    webscrap = finscrap.AssetsWrapper(FUNDS_JSON)
    webscrap.get_data()
    webscrap.out_dynamodb(DYNAMO_DB)
    return {"statusCode": 200}
