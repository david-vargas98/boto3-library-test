import boto3

client = boto3.client('s3') #s3 client
bucket_name = 'super-duper-new-bucket-1234' # bucket name

# ENCRYPTION

print(client.get_bucket_encryption(Bucket=bucket_name)) # - gets encryption information

# PUBLIC TEMP URL

url = client.generate_presigned_url(ClientMethod='get_object',  # - generates a public temp url for the file resource
                                    Params={'Bucket':'my-boto3-bucket-edgar', # bucket name
                                            'Key':'another_upload'}, # file name
                                            ExpiresIn=120) # it'll last 120 secs
print(url)

# DELETE OPERATIONS

client.delete_bucket(Bucket=bucket_name) # - deletes a bucket (bucket should be empty)

#if it's not empty, use resource to get all of the objects and delete them:
s3 = boto3.resource('s3')
bucket = s3.Bucket(bucket_name)
bucket.objects.all().delete() # be careful, this deletes EVERYTHING