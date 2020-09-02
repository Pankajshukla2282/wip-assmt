import json
import os
import boto3

ddb = boto3.resource('dynamodb')
_lambda = boto3.client('lambda')

# Get environment variable
table = ddb.Table(os.environ['TABLE_NAME'])

def handler(event, context):
    print('Request event: {}'.format(json.dumps(event)))

    actions = {
        'POST': lambda dynamo, x: dynamo.put_item(**x),
        'GET': lambda dynamo, x: dynamo.scan() #TODO: Work for data > 1MB
    }

    try:
        method = event['httpMethod']
        reqData = json.loads(event.get('body'))
        
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
