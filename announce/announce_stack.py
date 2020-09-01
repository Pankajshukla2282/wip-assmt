from aws_cdk import (
    aws_iam as iam,
    aws_apigateway as apigw,
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
    core
)

class AnnounceStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        #Create the API GW service role with permissions to call lambda
        api_role = iam.Role(
            self,
            "AnnounceAPIRole",
            assumed_by=iam.ServicePrincipal("apigateway.amazonaws.com"),
        )

        #Creating Lambda function for backend of API
        announce_lambda = _lambda.Function(self,'AnnounceLambda',
            handler='announce-handler.handler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
        )
 
        #refer https://pypi.org/project/aws-cdk.aws-apigateway/
        #Create an Lambda Rest API
        base_api = apigw.LambdaRestApi(self, 'AnnounceApiGW',
            handler=announce_lambda,
            rest_api_name='Announcements',
            description="This is a server for Announcement management.",
            proxy=False,
        )

        #Create API Integration Response object
        integration_response = apigw.IntegrationResponse(
            status_code="200",
            response_templates={"application/json": ""},
            response_parameters= {
                "method.response.header.Content-Type": "'application/json'",
                "method.response.header.Access-Control-Allow-Origin": "'*'",
                "method.response.header.Access-Control-Allow-Credentials": "'false'",
                "method.response.header.Access-Control-Allow-Headers": "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent'",
                "method.response.header.Access-Control-Allow-Methods": "'GET,POST'"
           },
        )

        #Create API Integration Options object for lambda   
        lambda_integration = apigw.LambdaIntegration(announce_lambda,
            proxy=False,
            credentials_role=api_role,
            content_handling=apigw.ContentHandling.CONVERT_TO_TEXT, # convert to base64
            request_parameters={
                "integration.request.header.Content-Type": "'application/x-www-form-urlencoded'",
            },
            integration_responses=[integration_response],
            passthrough_behavior=apigw.PassthroughBehavior.WHEN_NO_MATCH, #no suitable response template
            #request_templates={
            #    "application/json": "{\"httpMethod\": \"$context.httpMethod\",\"body\": \"$input.body\"}",
            #},
        )

        #valid response
        response_model = base_api.add_model("AnnounceAPIRespModel",
            content_type="application/json",
            model_name="AnnounceAPIRespModel",
            schema={
                "schema": apigw.JsonSchemaVersion.DRAFT4,
                "title": "AnnounceAPIResponse",
                "type": apigw.JsonSchemaType.OBJECT,
                "properties": {
                    "Items": {"type": apigw.JsonSchemaType.OBJECT}
                }
            }
        )

        # We define the JSON Schema for the transformed error response
        error_response_model = base_api.add_model("AnnounceAPIErrorRespModel",
            content_type="application/json",
            model_name="AnnounceAPIErrorRespModel",
            schema={
                "schema": apigw.JsonSchemaVersion.DRAFT4,
                "title": "errorResponse",
                "type": apigw.JsonSchemaType.OBJECT,
                "properties": {
                    "message": {"type": apigw.JsonSchemaType.STRING}
                }
            }
        )

        announce_model = base_api.add_model("AnnounceModel",
            content_type="application/json",
            model_name="AnnounceModel",
            schema={
                "type": apigw.JsonSchemaType.OBJECT,
                "properties": {
                    "atitle": {"type": apigw.JsonSchemaType.STRING},
                    "adescription": {"type": apigw.JsonSchemaType.STRING},
                    "adate": {"type": apigw.JsonSchemaType.STRING},
                    "astatus": {"type": apigw.JsonSchemaType.STRING}
                },
                "required": ["atitle"]
            }
        )

        #Create a resource named "announcement" on the base API
        api_resource = base_api.root.add_resource('announcement')

        announce_post = api_resource.add_method("POST", lambda_integration,
            request_models={
                "application/json": announce_model,
            },
            method_responses=[{
                #Successful
                "statusCode": "200",
                "responseParameters": {
                    "method.response.header.Content-Type": True,
                    "method.response.header.Access-Control-Allow-Headers": False,
                    "method.response.header.Access-Control-Allow-Methods": False,
                    "method.response.header.Access-Control-Allow-Origin": True,
                    "method.response.header.Access-Control-Allow-Credentials": False,
                },
                #Validate response
                "response_models": {
                    "application/json": response_model
                }
            }, {
                #error
                "statusCode": "400",
                "responseParameters": {
                    "method.response.header.Content-Type": True,
                    "method.response.header.Access-Control-Allow-Headers": False,
                    "method.response.header.Access-Control-Allow-Methods": False,
                    "method.response.header.Access-Control-Allow-Origin": True,
                    "method.response.header.Access-Control-Allow-Credentials": False,
                },
                #Validate response
                "response_models": {
                    "application/json": error_response_model
                }
            }]
        )

        announce_get = api_resource.add_method("GET", lambda_integration,
            method_responses=[{
                #Successful
                "statusCode": "200",
                "responseParameters": {
                    "method.response.header.Content-Type": True,
                    "method.response.header.Access-Control-Allow-Headers": False,
                    "method.response.header.Access-Control-Allow-Methods": False,
                    "method.response.header.Access-Control-Allow-Origin": True,
                    "method.response.header.Access-Control-Allow-Credentials": False,
                },
                #Validate response
                "response_models": {
                    "application/json": announce_model
                }
            }, {
                #error
                "statusCode": "400",
                "responseParameters": {
                    "method.response.header.Content-Type": True,
                    "method.response.header.Access-Control-Allow-Headers": False,
                    "method.response.header.Access-Control-Allow-Methods": False,
                    "method.response.header.Access-Control-Allow-Origin": True,
                    "method.response.header.Access-Control-Allow-Credentials": False,
                },
                #Validate response
                "response_models": {
                    "application/json": error_response_model
                }
            }]
        )

        api_req_key = base_api.add_api_key("AnnounceApiKey",
            api_key_name="MyAnnounceApiKey1",
            value="MyApiKeyThatIsAtLeast20Characters",
        )

        api_plan = base_api.add_usage_plan("AnnounceApiUsagePlan",
            name="Easy",
            api_key=api_req_key,
            throttle={
                "rate_limit": 10,
                "burst_limit": 2
            }
        )

        api_plan.add_api_stage(
            stage=base_api.deployment_stage,
            throttle=[{
                "method": announce_post,
                "throttle": {
                    "rate_limit": 5,
                    "burst_limit": 2
                }
            }, {
                "method": announce_get,
                "throttle": {
                    "rate_limit": 10,
                    "burst_limit": 2
                }
            }]
        )


        # create dynamo table
        table = ddb.Table(
            self, "announcements",
            partition_key=ddb.Attribute(
                name="atitle",
                type=ddb.AttributeType.STRING
            )
        )

        #Passing table name to Lambda Function
        announce_lambda.add_environment("TABLE_NAME", table.table_name)
        
        # grant permission to lambda to write to table
        table.grant_write_data(announce_lambda)
        
        # grant permission to lambda to read from table
        table.grant_read_data(announce_lambda)

        announce_lambda.grant_invoke(api_role)
        #announce_lambda.grantInvoke(new iam.ServicePrincipal('apigateway.amazonaws.com'))
