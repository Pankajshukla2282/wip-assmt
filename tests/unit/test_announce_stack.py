import json
import pytest

from aws_cdk import core
from announce.announce_stack import AnnounceStack

def get_template():
    app = core.App()
    AnnounceStack(app, "announce")
    return json.dumps(app.synth().get_stack("announce").template)

def test_api_resource_created():
    assert("AWS::ApiGateway::Resource" in get_template())

def test_lambda_function_created():
    assert("AWS::Lambda::Function" in get_template())

def test_dynamodb_table_created():
    assert("AWS::DynamoDB::Table" in get_template())
