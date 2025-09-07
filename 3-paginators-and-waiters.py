import boto3

s3 = boto3.client('s3') #s3 client

paginator = s3.get_paginator('list_objects_v2') #create paginator

results = paginator.paginate(Bucket='my-boto3-bucket-edgar') #result are retrieve

print(list(results), "\n") # we get the list of objects

for item in results.search('Contents'): #prints the dictionary
    print(item)

for item in results.search('Contents'): #prints the key's value
    print(item['Key'])

##### WAITERS: e

bucket_name = 'super-duper-new-bucket-1234' # bucket name

waiter = s3.get_waiter('bucket_exists') # will wait until certain bucket exists

wait_config = {'Delay': 10, 'MaxAttempts':40} # my wait configuration (400 secs)

print(f'Waiting for the bucket: {bucket_name}')
waiter.wait(Bucket=bucket_name, WaiterConfig=wait_config) # it will wait until the bucket is created
print('The bucket has been made')