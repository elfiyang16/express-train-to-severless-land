import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

"""
Demonstration of using Hash + Range Key
"""

def create_table_with_range():
    table = dynamodb.create_table(
        TableName='Books',
        KeySchema=[
            {
                'AttributeName': 'title',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'author',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'author',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1,
        }
    )

    print("Table status:", table.table_status)
    
def create_books():
    book = {
        'title': "This is a Good Book",
        'author': 'Jon Doe',
        'year': '1980'
    }
    
    another_book = {
        'title': "This is a Good Book",
        'author': 'Jane Doe',
        'year': '1998'
    }    
    table = dynamodb.Table('Books')
    
    table.put_item(Item=book)
    table.put_item(Item=another_book)
    
    

def fetch_data_with_range():    
    table = dynamodb.Table('Books')      
    resp = table.get_item(
            Key={
                'title' : 'This is a Good Book',
                'author': 'Jane Doe'
            }
        )              
    print(resp['Item'])
    #{'year': '1998', 'title': 'This is a Good Book', 'author': 'Jane Doe'}
 
    resp = table.query(
        KeyConditionExpression=
            Key('title').eq('This is a Good Book') & Key('author').eq('Jon Doe')
    )
 
    print(resp['Items'][0])
    #{'year': '1980', 'title': 'This is a Good Book', 'author': 'Jon Doe'}

