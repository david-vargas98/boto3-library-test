import boto3

#RUN THIS SCRIPT WHEN WAITING FOR BUCKET TO BE CREATED

bucket_name = 'super-duper-new-bucket-1234' # bucket name

s3 = boto3.resource('s3')

s3.create_bucket(Bucket=bucket_name)

