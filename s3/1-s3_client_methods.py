import boto3

client = boto3.client('s3') #s3 client

client.create_bucket(Bucket='my-boto3-bucket-edgar') #bucket creation

with open('1-myFile.txt', 'w') as file:             #file creation
    file.write('This is a test file for upload')

client.upload_file(Filename='1-myFile.txt',         #file upload
                   Bucket='my-boto3-bucket-edgar',
                   Key='test-upload-file')

client.download_file(Bucket='my-boto3-bucket-edgar', #file download
                     Key='test-upload-file',
                     Filename='1-my-local-download.txt')

with open('1-my-local-download.txt', 'r') as file:     #read downloaded file
    print(file.read())

client.delete_object(Bucket='my-boto3-bucket-edgar', #delete bucket file
                     Key='test-upload-file')