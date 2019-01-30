import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    if 'body' not in event:
        return {
            'statusCode': 400,
            'headers': {
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Credentials" : "true"
             },
            'body': json.dumps("Empty Body")
        }
    entry = json.loads(event['body'])
    #entry = event['body']
    
    print (entry)

    if 'city' not in entry or 'category' not in entry or 'section' not in entry or 'name' not in entry or 'address' not in entry:
        return {
            'statusCode': 400,
            'headers': {
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Credentials" : "true"
             },
            'body': json.dumps("Invalid Data")
        }
    
    cities = dynamodb.Table("cities")
    result = cities.get_item(Key={
        "name": entry['city'],
        "category": entry['category']
    })
    
    if 'Item' not in result:
        return {
            'statusCode': 404,
            'headers': {
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Credentials" : "true"
             },
            'body': json.dumps("City or Category is not found")
        }

    if entry['section'] not in result['Item']['sections']:
        return {
            'statusCode': 400,
            'headers': {
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Credentials" : "true"
             },
            'body': json.dumps("Section not found")
        }

    city = dynamodb.Table(entry['city'])
    result = city.get_item(Key={
        "category": entry['category'],
        "section": entry['section']
    })
    
    if 'Item' in result:
        response = city.update_item(
            Key={"category":entry['category'],"section":entry['section']},
            UpdateExpression="SET entries = list_append(entries, :e)", 
            ExpressionAttributeValues={
                ":e": [entry]
            },
            ReturnValues="UPDATED_NEW"
        )
    else:
        response = city.put_item(Item = {
            "category": entry['category'],
            "section": entry['section'],
            "entries": [entry]
        })
        
    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Credentials" : "true"
         },
        'body': json.dumps(response)
    }