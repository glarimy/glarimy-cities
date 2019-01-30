import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
    
def lambda_handler(event, context):
    table = dynamodb.Table('cities')
    response = table.scan()
    #    ProjectionExpression="#name", 
    #    ExpressionAttributeNames={ "#name": "name" }
    #)
    
    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Credentials" : "true"
         },
        'body': json.dumps(response)
    }
