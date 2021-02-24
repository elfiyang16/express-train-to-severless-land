import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

def create_table_with_gsi():
    table = dynamodb.create_table(
        TableName='Employees',
        KeySchema=[
            {
                'AttributeName': 'emp_id',
                'KeyType': 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'emp_id',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'email',
                'AttributeType': 'S'
            },
    
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'email',
                'KeySchema': [
                    {
                        'AttributeName': 'email',
                        'KeyType': 'HASH'
                    },
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput' :{
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1,
                }
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1,
        }
    )

    print("Table status:", table.table_status)
    
def create_employee():
    user = {
        'emp_id': 1,
        'first_name': 'Jon',
        'last_name': 'Doe',
        'email': 'jdoe@test.com'
    }
    
    dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.Table('Employees')
    
    table.put_item(Item=user)
    


def query_data_with_gsi():    
    table = dynamodb.Table('Employees')
    
    response = table.query(
        IndexName='email',
        KeyConditionExpression=Key('email').eq('jdoe@test.com')
    )
    
    print(response['Items'][0])
    #{'last_name': 'Doe', 'email': 'jdoe@test.com', 'first_name': 'Jon', 'emp_id': Decimal('1')}

def create_table_with_lsi():    
    table = dynamodb.create_table(
        TableName='Posts',
        KeySchema=[
            {
                'AttributeName': 'user_name',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'title',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'user_name',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'subject',
                'AttributeType': 'S'
            },
    
        ],
        LocalSecondaryIndexes=[
            {
                'IndexName': 'user_name_subject',
                'KeySchema': [
                    {
                        'AttributeName': 'user_name',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'subject',
                        'KeyType': 'RANGE'
                    },
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1,
        }
    )

    print("Table status:", table.table_status)

def create_posts():
    post1 = {
        'title': "My favorite hiking spots",
        'user_name': 'jon_doe',
        'subject': 'hiking'
    }
    
    post2 = {
        'title': "My favorite recipes",
        'user_name': 'jon_doe',
        'subject': 'cooking'
    }
    
    post3 = {
        'title': "I love hiking!",
        'user_name': 'jane_doe',
        'subject': 'hiking'
    }
    
    dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.Table('Posts')
    
    table.put_item(Item=post1)
    table.put_item(Item=post2)
    table.put_item(Item=post3)