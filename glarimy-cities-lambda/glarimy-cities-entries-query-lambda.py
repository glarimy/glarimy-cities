import json
import boto3

dynamodb = boto3.client('dynamodb')
    
def lambda_handler(event, context):
    city = event['queryStringParameters']['city']
    category = event['queryStringParameters']['category']
    section = event['queryStringParameters']['section']
    #city = 'Tanuku'
    #category = 'Health'
    #section = 'Hospitals'
    response = dynamodb.get_item(TableName=city, Key={'category':{'S':category}, 'section':{'S':section}})
    
    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Credentials" : 'true'
         },
        'body': json.dumps(response)
    }