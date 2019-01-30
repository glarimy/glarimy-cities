import json
import boto3

dynamodb = boto3.resource('dynamodb')

def addCity(city):
    table = dynamodb.Table("cities")
    result = table.get_item(Key={
        "name": city,
        "category": "Default"
    })
    if 'Item' in result:
        raise Exception({
            "code": 409,
            "message": "City is already present"
            })
    else:
        response = table.put_item(Item = {
            "name": city, 
            "category": 'Default',
            "sections": []
        })
        return response

def addCategory(city, category):
    table = dynamodb.Table("cities")
    result = table.get_item(Key={
        "name": city,
        "category": category
    })
    if 'Item' in result:
        raise Exception({
            "code": 409,
            "message": "Category is already present"
            })
    else:
        response = table.put_item(Item = {
            "name": city, 
            "category": category,
            "sections": []
        })
        return response

def addSection(city, category, section):
    table = dynamodb.Table("cities")
    result = table.get_item(Key={
        "name": city,
        "category": category
    })
    if 'Item' not in result:
        raise Exception({
            "code": 404,
            "message": "Category not found"
            })
    else:
        if section in result['Item']['sections']:
            raise Exception({
                "code": 409,
                "message": "Section is already present"
                })

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

    try:     
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
    except Exception as e:
        return {
            'statusCode': e.code,
            'headers': {
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Credentials" : "true"
             },
            'body': json.dumps(e.message)
        }