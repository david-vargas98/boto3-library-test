import boto3

client = boto3.client('dynamodb') # CLIENT examples

# variables
tableName = 'Movies'

# ------------------- BATCH OPERATIONS

# all of the movies to insert
movies = [
    {
        'Title': 'The Matrix 2',
        'Director': 'Lana Wachowski',
        'Year':'2003',
        'Rating':'4.6'
    },
    {
        'Title': 'The Matrix 3',
        'Director': 'Lana Wachowski',
        'Year':'2003',
        'Rating':'4.5'
    },
    {
        'Title': 'Inception',
        'Director': 'Christopher Nolan',
        'Year':'2010',
        'Rating':'4.6'
    },
    {
        'Title': 'Saving Private Ryan',
        'Director': 'Steven Spielberg',
        'Year':'1999',
        'Rating':'4.7'
    }
]

# batch request initialization
batch__request = []
print(f"\tInitial batch_request:\n{batch__request}\n")

# building the batch request
print("\tBuilt batch_request:")
for movie in movies:
    batch__request.append({
        'PutRequest':{
            'Item':{
                'Title':{'S':movie['Title']},
                'Rating':{'N':str(movie['Rating'])},
                'Director':{'S':movie['Director']},
                'Year':{'N':str(movie['Year'])}
            }
        }
    })

print(f"{batch__request}\n")

# making request to dynamodb
print("\tMaking batch_request to the database...\n\tResults:\n")

response = client.batch_write_item(RequestItems={tableName:batch__request})

print(f"{response}\n")

# making a get batch request from dynamodb
print("\tMaking get batch_request to the database...\n")

batch__request_get = {'Keys': []}
print(f"\tInitial get batch_request:\n{batch__request_get}\n")

print("\tBuilt get batch_request:")
for movie in movies:
    batch__request_get['Keys'].append({
        'Title':{'S': movie['Title']},
        'Rating':{'N': str(movie['Rating'])}
    })

print(f"{batch__request_get}\n")

print("\tMaking get batch_request...")

batch__request_get_response = client.batch_get_item(RequestItems={tableName: batch__request_get}) 

print(batch__request_get_response)

# ------------------- NOTE: If you want more than 1 MB size response, then you need to start paginating, check DOCS

# ------------------- SCAN: it reads ALL OF THE ELEMENTS from a table, **it could be slow and inefficient**

items = []
response = client.scan(TableName=tableName) # get all the elements (1 MB data limit)
items.extend(response['Items']) # response['Items'] contains the first elements extend add the elements to the list

print(f"\nItems without pagination:\n {items}")

# pagination (BE CAREFUL if it's a large table, since it could be running forever and you gonna have a huge list in memory)
while "LastEvaluatedKey" in response.keys(): # if response has 'LastEvaluatedKey' it means there is more data to read
    response = client.scan(TableName=tableName, ExclusiveStartKey=response['LastEvaluatedKey']) # continues the scan from where it left off
    items.extend(response['Items']) # it stills adding elements to the list until 'LastEvaluatedKey' is missing
print(f"\nItems with pagination:\n {items}")

# ------------------- Filtering
print("\nFiltering records...")
filteredRecords = client.scan(
    TableName=tableName,
    FilterExpression='Rating >= :num ',
    ExpressionAttributeValues={':num':{'N':'4.7'}}
)
print(filteredRecords)


# ----------------- using Attr
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table(tableName)

# print(dir(Attr))

record_Attr = table.scan(
    FilterExpression=Attr('Rating').gte(Decimal(4.5))
)

print(record_Attr)

print(table.key_schema)

print(client.describe_table(TableName=tableName))

# delete the table
table.delete()