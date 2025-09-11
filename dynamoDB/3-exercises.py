#In this exercise you are going to create a db using "Netflix Movies an TV Shows" using the provided csv file
with open("netflix_titles.csv", "r", encoding='utf-8') as file:
    lines = file.readlines()

# print(lines[:5])

import boto3
import csv

client = boto3.client('dynamodb')

#variables
table_name = 'Movies_Exercise'

# task #01: create the table attributes and its schema. Use show_id as the partition key and release_year as range_key. Use 10 for both,
# read and write capacity units.
key_schema = [
    {
        'AttributeName':'show_id',
        'KeyType':'HASH'
    },
    {
        'AttributeName':'release_year',
        'KeyType':'RANGE'
    }
]

attribute_definitions = [
    {
        'AttributeName':'show_id',
        'AttributeType':'S'
    },
    {
        'AttributeName':'release_year',
        'AttributeType': 'N'
    },
]

provisioned_throughput = {
    'ReadCapacityUnits':10,
    'WriteCapacityUnits':10
}

# print("\tCreating table...")
# table_creation = client.create_table( # table creation
#     TableName= table_name,
#     KeySchema= key_schema,
#     AttributeDefinitions= attribute_definitions,
#     ProvisionedThroughput= provisioned_throughput
# )
# print(table_creation)

# task #02: we want to use GSI, to be able to query for the "Country" - create the table with the above schema and the secondary index
# print("\tUpdating table...")
# table_update = client.update_table(
#     TableName= table_name,
#     AttributeDefinitions= attribute_definitions,
#     GlobalSecondaryIndexUpdates= [{
#         'Create':{
#             'IndexName':'idx_country',
#             'KeySchema':key_schema,
#             'Projection':{
#                 'ProjectionType':'ALL'
#             },
#             'ProvisionedThroughput': provisioned_throughput
#         }
#     }]
# )
# print(f"\nUpdate response:\n{table_update}")

# task 1 and 2 in a single one:

gsi_key_schema = [{
    'AttributeName':'country',
    'KeyType':'HASH'
}]

attribute_definitions.append({
    'AttributeName': 'country',
    'AttributeType':'S'
})

global_secondary_idx = [{
    'IndexName':'idx_country',
    'KeySchema':gsi_key_schema,
    'Projection':{
        'ProjectionType':'ALL'
    },
    'ProvisionedThroughput': provisioned_throughput
}]

print("\tCreating table with GSI...")
table_creation = client.create_table( # table creation
    TableName= table_name,
    KeySchema= key_schema,
    AttributeDefinitions= attribute_definitions,
    ProvisionedThroughput= provisioned_throughput,
    GlobalSecondaryIndexes= global_secondary_idx
)
print(table_creation)

waiter = client.get_waiter('table_exists') # wait for table creation

print(f"\n\tWaiting for '{table_name}' table to be created...")
waiter.wait(
    TableName= table_name,
    WaiterConfig= {
        'Delay': 60,
        'MaxAttempts':10
    }
)
print(f"Table '{table_name}' was created...")


# task #03: read the data from the csv file to a list of dictionaries
movies_list = []
with open('netflix_titles.csv', mode='r', encoding='utf-8') as input_file:
    reader = csv.DictReader(input_file)
    for row in reader:
        movies_list.append(row)

#print(movies_list[:5])

# task #04: create the batch requests to upload the data. Note, that batch requests can only
# handle 25 items at once. Add the data types accordingly to the elements.
# As we set 'ProvisionedThroughput' to a low value of 10 this might take a while as 
# aws throttles the writing operations (but is very cheap)

batch_movies_request = []
counter = 0

print("\nMaking batch movie request...")

with open('netflix_titles.csv', mode='r', encoding='utf-8') as input_file:
    movies_reader = csv.DictReader(input_file) # handles header rows and converts them into keys 
    for movie in movies_reader:
        country_value = movie['country']
        if not country_value:
            country_value = "Unknown"
        
        batch_movies_request.append({
            'PutRequest':{
                'Item':{
                    'show_id':{'S':movie['show_id']},
                    'release_year':{'N':movie['release_year']},
                    'type':{'S':movie['type']},
                    'title':{'S':movie['title']},
                    'director':{'S':movie['director']},
                    'cast':{'S':movie['cast']},
                    'country':{'S':country_value},
                    'date_added':{'S':movie['date_added']},
                    'rating':{'S':movie['rating']},
                    'duration':{'S':movie['duration']},
                    'listed_in':{'S':movie['listed_in']},
                    'description':{'S':movie['description']}
                }
            }
        })

        counter+=1

        if counter % 25 == 0:
            print(f"\n\tUploading 25 movies batch...{counter} movies processed")
            
            response = client.batch_write_item(RequestItems={table_name:batch_movies_request})
            print("\nMovies uploaded successfully!")

            batch_movies_request = []
    
    if len(batch_movies_request) > 0:
        print(f"\nThere {len(batch_movies_request)} movies left.\n\tUploading the rest of the movies...")
        
        response = client.batch_write_item(RequestItems={table_name:batch_movies_request})
        print(f"The last batch was uploaded successfully. Total movies: {counter} ")

# task 05: what is the name of the show with show id 10
print("\nRequesting item with both keys...")
item_key = {
    'show_id':{'S':'s10'},
    'release_year':{'N':'2021'}
}

show_id10 = client.get_item(
    TableName= table_name,
    Key= item_key
)

print(f"The item with 'show_id' equals to 10 is:\n {show_id10}")

print("\nRequesting item only with 'show_id' key (using query)...")

show_id10_response = client.query(
    TableName= table_name,
    KeyConditionExpression='show_id = :id',
    ExpressionAttributeValues={':id':{'S':'s10'}}
)
print(show_id10_response)

# # task #06: what shows are from germany? Hint: you need to pass IndexName to the query function
print("\nGetting shows from germany...")

germany_shows = client.query(
    TableName= table_name,
    KeyConditionExpression='country = :c',
    ExpressionAttributeValues={':c':{'S':'Germany'}},
    IndexName='idx_country'
)

print(germany_shows)

# task #07: what shows are from India and from 2021 or later?
print("\nGetting shows from india and from 2021 or later (inefficient)...")
movie_items = []
india_scan_response = None

while True:
    if india_scan_response:
        # LastEvaluatedKey tells us the last key that was read
        india_scan_response = client.scan(
            TableName= table_name,
            FilterExpression= 'country = :c AND release_year >= :ry',
            ExpressionAttributeValues={
                ':c':{'S':'India'},
                ':ry':{'N':'2021'}
            },
            ExclusiveStartKey=india_scan_response['LastEvaluatedKey']
        )
    else:
        # first call to scan
        india_scan_response = client.scan(
            TableName= table_name,
            FilterExpression= 'country = :c AND release_year >= :ry',
            ExpressionAttributeValues={
                ':c':{'S':'India'},
                ':ry':{'N':'2021'}
            }
        )
    
    # append elements
    movie_items.extend(india_scan_response['Items'])

    # no more keys to read?
    if 'LastEvaluatedKey' not in india_scan_response:
        break

print(f"\nTotal count from scan: {len(movie_items)}")
print(movie_items)

# task #08: can you also perform this operation using a query?
# yes, by using resource and applying Key and Attr:
from boto3.dynamodb.conditions import Key, Attr

dynamodb_resource = boto3.resource('dynamodb')
table = dynamodb_resource.Table(table_name)

print("\nGetting shows from india and from 2021 or later...\n")

movie_items_query = []
india_query_response = None

while True:
    if india_query_response:
        india_query_response = table.query(
            IndexName='idx_country',
            KeyConditionExpression=Key('country').eq('India'),
            FilterExpression=Attr('release_year').gte(2021),
            ExclusiveStartKey=india_query_response.get('LastEvaluatedKey')
        )
    else:
        india_query_response = table.query(
            IndexName='idx_country',
            KeyConditionExpression=Key('country').eq('India'),
            FilterExpression=Attr('release_year').gte(2021)
        )

    movie_items_query.extend(india_query_response['Items'])

    if 'LastEvaluatedKey' not in india_query_response:
        break

print(f"Total count from query: {len(movie_items_query)}")
print(india_query_response['Items'])

# task #08: delete the table
table.delete()
print("\nThe table was deleted")