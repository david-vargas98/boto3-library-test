import boto3

client = boto3.client('dynamodb') # CLIENT examples

# table definition
table_name = 'Movies'
attributes = [
    {
        'AttributeName':'Title',
        'AttributeType':'S'
    },
    {
        'AttributeName':'Rating',
        'AttributeType':'N'
    }
]

key_schema = [
    {
        'AttributeName':'Title',
        'KeyType':'HASH'
    },
    {
        'AttributeName':'Rating',
        'KeyType':'RANGE'
    }
]

provisioned_throughput = {
    'ReadCapacityUnits': 5,
    'WriteCapacityUnits':5
}

# table creation
# response = client.create_table(TableName= table_name,
#                                AttributeDefinitions= attributes,
#                                KeySchema= key_schema,
#                                ProvisionedThroughput= provisioned_throughput)

# print(response)

# new record definition
print("\n\tRecord creation:")
record = {
    'Title': {'S': 'The Matrix'},
    'Director':{'S':'Lana Wachowski'},
    'Year':{'N':'1999'},
    'Rating':{'N':'5'}
}

# # new record creation
record_creation = client.put_item(TableName=table_name, Item=record)

print(record_creation)

# getting item key creation
item_key = {
    'Title':{'S':'The Matrix'},
    'Rating': {'N': '5'}
}

query = client.get_item(TableName=table_name, Key=item_key)

print(query['Item'])

# update record
update = 'SET Director = :r'

update_record = client.update_item(
    TableName=table_name,
    Key=item_key,
    UpdateExpression=update,
    ExpressionAttributeValues={
        ':r':{'S':'Lana and Lilly Wachowski'}
    }
)

print(f"Record updated:\n{update_record}")

# querying the updated record
print("\nGetting the updated record again:")

query = client.get_item(TableName=table_name, Key=item_key)

print(query['Item'])

# deleting record
print(f"\nRecord deleted:")
deleted = client.delete_item(TableName=table_name, Key=item_key)
print(deleted)