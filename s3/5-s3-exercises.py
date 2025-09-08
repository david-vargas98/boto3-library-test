import boto3
from botocore.exceptions import ClientError
import os

# client and resource
client = boto3.client('s3')
resource = boto3.resource('s3')

#Common variables
bucket_name = 'my-task-bucket-edgar'
file_name = '5-my-task-file.txt'
key_file_name = 'my_uploaded_task_file.txt'

#task 1: list all buckets
print("\t#01 task - list of buckets:")
try:
    response = client.list_buckets() # dictionary with keys 'ResponseMetadata', 'Buckets' and 'Owner'
    for bucket in response['Buckets']: # 'Buckets' is a list of dictionaries, each of them represents a single bucket
        print(bucket['Name'])          # we access the key 'Name' for each bucket
except ClientError as e:
    print(f"Error while listing buckets: {e}")

#task 2: create a new bucket of your choice
print("\n\t#02 task - create a new bucket:")
try:
    client.create_bucket(Bucket=bucket_name)
    print(f"The '{bucket_name}' bucket was created\n")
except ClientError as e:
    if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
        print(f"Bucket '{bucket_name} already  exists. Sorry...'")
    else:
        print(f"Error creating bucket: {e}")
        exit()

#task 3: create a text file and upload it to your bucket
print("\t#03 task - create text file and upload it to s3:")
try:
    with open(file_name, 'w') as taskFile:
        taskFile.write('My file is now created :D')
    print("...file created")

    client.upload_file(file_name, bucket_name, key_file_name)
    print(f"the '{file_name}' file was uploaded correctly and named as '{key_file_name}'\n")
except FileNotFoundError:
    print(f"Error: The local file '{file_name}' was not found")
except ClientError as e:
    print(f"Error uploading file: {e}")

#task 4: List all objects in your bucket
print(f"\t#04 task - list all objects from '{bucket_name}' s3 bucket:")

try:
    paginator = client.get_paginator('list_objects')
    pages = paginator.paginate(Bucket=bucket_name)

    found_objects = False # flag

    for page in pages:
        for obj in page.get('Contents', []):
            print(f"Object Key: {obj['Key']}")
            found_objects = True # yes, there are
    
    if not found_objects:
        print("No objects were found in the bucket.")

except ClientError as e:
    print(f"Error listing objects: {e}")

#task 5: create a URL so your friend can download the file within the next 5 minutes
print(f"\t#05 task - generate a URL to download a file:")
try:
    url = client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket_name, 
            'Key': key_file_name},
        ExpiresIn=60
        )

    print(f"...the url was created\nUrl...: {url}\n")
except ClientError as e:
    print(f"Error generating presigned URL: {e}")

#task 6: download the objects and delete it after
print(f"\t#06 task - download the objects and delete it after:")
try:
    downloaded_file_name = '5-my-downloaded-file.txt'
    with open(file_name, 'wb') as data:
        client.download_fileobj(bucket_name, key_file_name, data)
    print(f"The file was successfully download to '{file_name}' :D\n")

    # clean up files
    os.remove(file_name)
    print(f"Local file '{file_name}' was deleted.")
except ClientError as e:
    print(f"Error downloading file: {e}")
except FileNotFoundError:
    print(f"Error: Local file '{downloaded_file_name}' not found after download.")

#task 7: delete the bucket
print(f"\t#07 task - Delete the bucket D: :")
try:
    # using s3 resource to delete all objects in the bucket first
    bucket = resource.Bucket(bucket_name)
    bucket.objects.all().delete()
    print(f"All objects in bucket '{bucket_name}' hav been deleted.")

    # after, we delete the bucket itself
    bucket.delete()
    print(f"Bucket '{bucket_name}' was deleted successfully.")
except ClientError as e:
    print(f"Error deleting bucket: {e}")


# ---------------- Using client (more steps, verbose, etc):

# delete_paginator = client.get_paginator('list_objects')
# results = client.list_objects_v2(Bucket=bucket_name)

# print(results)

# if 'Contents' in results:
#     print(f"The '{bucket_name}' bucket has objects in it.\nThe objects will be deleted first...\n")
#     deleteObjsResponse = client.delete_objects(Bucket=bucket_name, Delete={'Objects': [{'Key': key_file_name}]})
#     print("The objects were deleted successfully!")

# deleteResponse = client.delete_bucket(
#     Bucket= bucket_name,
# )

# print(f"The '{bucket_name}' bucket was deleted:\n", deleteResponse)
