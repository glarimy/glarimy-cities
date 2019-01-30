import json
import boto3

dynamodb = boto3.resource('dynamodb')

def addCity(city):
    table = dynamodb.Table("cities")
    response = table.put_item(Item = {
        "name": city, 
        "category": 'Default',
        "sections": []
    })
    return response

def addCategory(city, category):
    table = dynamodb.Table("cities")
    response = table.put_item(Item = {
        "name": city, 
        "category": category,
        "sections": []
    })
    return response

def addSection(city, category, section):
    table = dynamodb.Table("cities")
    response = table.update_item(
        Key={"name":city,"category":category},
        UpdateExpression="SET sections = list_append(sections, :e)", 
        ExpressionAttributeValues={
            ":e": [section]
        },
        ReturnValues="UPDATED_NEW"
    )
    return response
    
def lambda_handler(event, context):
    #verify if params are passed
    if 'queryStringParameters' not in event:
        return {
            'statusCode': 400,
            'headers': {
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Credentials" : "true"
             }
        }
        
    #verify if city is passed
    if 'city' not in event['queryStringParameters'] or event['queryStringParameters']['city'] is None:
        return {
            'statusCode': 400,
            'headers': {
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Credentials" : "true"
             }
        }
        
    city = event['queryStringParameters']['city']
    
    if 'category' not in event['queryStringParameters'] or event['queryStringParameters']['category'] is None:
        response = addCity(city)
    else:
        if 'section' not in event['queryStringParameters'] or event['queryStringParameters']['section'] is None:
            category = event['queryStringParameters']['category']
            response = addCategory(city, category)
        else:
            category = event['queryStringParameters']['category']
            section = event['queryStringParameters']['section'] 
            response = addSection(city, category, section)

    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Credentials" : "true"
         },
        'body': json.dumps(response)
    }