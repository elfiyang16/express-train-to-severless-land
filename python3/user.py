import boto3
from boto3.dynamodb.conditions import Key


dynamodb = boto3.resource('dynamodb')


def create_table():
    table = dynamodb.create_table(
        TableName='Users',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1,
        }
    )

    print("Table status:", table.table_status)
  

def create_user():
    user = {
        'id': 1,
        'first_name': 'Jon',
        'last_name': 'Doe',
        'email': 'jdoe@test.com'
    }
        
    table = dynamodb.Table('Users')
    table.put_item(Item=user)

def create_bunch_of_users():    
    table = dynamodb.Table('Users') 
    
    for n in range(3):
        table.put_item(Item={
            'id': n,
            'first_name': 'Jon',
            'last_name': 'Doe' + str(n),
            'email': 'jdoe'+ str(n) +'@test.com'
        })
        
def get_item():    
    table = dynamodb.Table('Users')      
    resp = table.get_item(
            Key={
                'id' : 1,
            }
        )
                
    if 'Item' in resp:
        print(resp['Item'])

    #{'id': Decimal('1'), 'email': 'jdoe@test.com', 'last_name': 'Doe', 'first_name': 'Jon'}
    
    
def query():    
    table = dynamodb.Table('Users')      
    resp = table.query(
        KeyConditionExpression=Key('id').eq(1)
    )
                
    if 'Items' in resp:
        print(resp['Items'][0])
        
#{'id': Decimal('1'), 'email': 'jdoe@test.com', 'last_name': 'Doe', 'first_name': 'Jon'}

def update():    
    table = dynamodb.Table('Users')
    
    table.update_item(
        Key={
                'id': 1,
            },
        UpdateExpression="set first_name = :g",
        ExpressionAttributeValues={
                ':g': "Jane"
            },
        ReturnValues="UPDATED_NEW"
        )
        
    get_item()
    #{'email': 'jdoe@test.com', 'id': Decimal('1'), 'last_name': 'Doe', 'first_name': 'Jane'}


def delete_user():    
    table = dynamodb.Table('Users')
    
    response = table.delete_item(
        Key={
            'id': 1,
        },
    )
    

def scan_first_and_last_names():
    """
    ProjectionExpression: so that Scan only returns some of the attributes, rather than all of them.
    """    
    table = dynamodb.Table('Users')
    resp = table.scan(ProjectionExpression="first_name, last_name")
    print(resp['Items'])
    
    '''
    [
      {'last_name': 'Doe2', 'first_name': 'Jon'}, 
      {'last_name': 'Doe1', 'first_name': 'Jon'}, 
      {'last_name': 'Doe0', 'first_name': 'Jon'}
    ]
    '''
    
    
def multi_part_scan():
    """
    Scans have a 1mb limit on the data returned. 
    If we think we’re going to exceed that, 
    we should continue to re-scan and pass in the LastEvaluatedKey:
    """    
    table = dynamodb.Table('Users')

    response = table.scan()
    result = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        result.extend(response['Items'])
    
    
    