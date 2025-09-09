import boto3

client = boto3.client('dynamodb')

# table definition
table_name = 'Movies'
attributes = [
    {
        'AttributeName':'Title',
        'AttributeType':'S'
    }
]