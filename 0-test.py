import boto3

s3 = boto3.resource('s3') # create the s3 resource
buckets = list(s3.buckets.all()) # getting buckets from s3 resource into a list

# if there are any buckets, we show them, if not, we show a message
if buckets:
    for bucket in buckets:
        print(bucket.name)
else:
    print("There's no buckets")