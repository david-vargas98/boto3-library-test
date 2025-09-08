import boto3

s3 = boto3.resource('s3') #s3 resource

print(list(s3.buckets.all())) #print all s3 buckets

bucket = s3.Bucket(name='my-boto3-bucket-edgar') #we get a specific bucket as an object

bucket.upload_file(Filename='1-myFile.txt', Key='another_upload') #uploading a file

print(bucket.objects.all()) #prints the object

bucket.download_file(Filename='2-some_new_download.txt', Key='another_upload') #download a specific file

print(list(bucket.objects.filter(Prefix='another'))) # gets an object which starts with 'another'

print(list(bucket.objects.filter(Prefix='mine'))) # gets an empty list
