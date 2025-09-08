import boto3

client = boto3.client('pricing')

# getting prices for s3 service
paginator = client.get_paginator('describe_services')

# first we need to look up for the real service codes for the services 
for page in paginator.paginate():
    for service in page['Services']:
        print(service['ServiceCode'])

# result using the service code
result = client.get_products(
    ServiceCode='AmazonS3',
    Filters=[
        {'Type': 'TERM_MATCH',
         'Field': 'regionCode',
         'Value': 'us-east-1'}
    ]
)

print(result)

# This could be quiet complex, so it's always recommended to just google it xdd