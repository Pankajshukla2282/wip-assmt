import json
import decimal
import os
import boto3

ddb = boto3.resource('dynamodb')
_lambda = boto3.client('lambda')

# Get environment variable
table = ddb.Table(os.environ['TABLE_NAME'])

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def handler(event, context):
    print('Request event: {}'.format(json.dumps(event)))

    actions = {
        'POST': lambda dynamo, x: dynamo.put_item(**x),
        'GET': lambda dynamo, x: json.dumps(dynamo.scan(), indent=4, cls=DecimalEncoder) #TODO: Work for data > 1MB
    }

    try:
        method = event['httpMethod']
        reqData = event.get('body')
        
        payload = {"Item": reqData}
        
        if method in actions:
            outParams = actions[method](table, payload)
        else:
            raise ValueError('Unrecognized method "{}"'.format(method))

        resp = outParams

        return {
            "isBase64Encoded": "'true'",
            "statusCode": 200,
            "headers": { "Content-Type": "application/json"},
            "body": resp
        }
    except Exception as e:
        return {
            "isBase64Encoded": "'true'",
            "statusCode": 200,
            "headers": { "Content-Type": "application/json"},
            "body": "{c}: {m}".format(c = type(e).__name__, m = str(e))
        }
