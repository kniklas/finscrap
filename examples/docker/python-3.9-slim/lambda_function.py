# pylint: disable=missing-module-docstring
import sys
from lxml import etree


# pylint: disable=unused-argument
def handler(event, context):
    """Sample pure Lambda function"""
    print(__name__)
    print(etree.LXML_VERSION)
    return "Hello from AWS Lambda using Python" + sys.version + "!"
