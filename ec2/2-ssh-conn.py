import boto3
from botocore.exceptions import ClientError 
import paramiko

client = boto3.client('ec2')
fileName = 'my-key-par.pem'

print("\tCreating key...")
try:
    key_pair = client.create_key_pair(KeyName='new-course-key-pair') # creating a key pair

    private_key = key_pair['KeyMaterial'] # generate private key for ssh connection

    with open(fileName, 'w') as file: # writing the private key into a PEM file
        file.write(private_key)
except ClientError as e:
    if e.response['Error']['Code'] == 'InvalidKeyPair.Duplicate':
        print("Error: The key already exists.")


security_groups = client.describe_security_groups() # getting the GroupId from security groups
print(security_groups['SecurityGroups'], "\n")

ec2 = boto3.resource('ec2') # using resource for instance creation 

# instance = ec2.create_instances( #instance creation
#     MinCount=1,
#     MaxCount=1,
#     InstanceType='t3.micro',
#     ImageId='ami-0fd3ac4abb734302a',
#     KeyName='new-course-key-pair',
#     SecurityGroupIds=['sg-0993a335a7ba327e3']
# )

# print(instance)

# HERE WE USE Paramiko to ssh client connection (kinda outside the boto3 scope)
ssh = paramiko.SSHClient()

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)

private_key = paramiko.RSAKey(filename=fileName)

# getting ip address from the instance
description = client.describe_instances(InstanceIds=['i-0b3c09b8f05555028']) # instance id was grabbed from the instance creation

ip_address_instance = description['Reservations'][0]['Instances'][0]['PublicIpAddress']
print(ip_address_instance)

print("\nConnecting to the instance...")
ssh.connect(hostname=ip_address_instance, username='ec2-user', pkey=private_key) # You need to add an inbound rule to the sg to allow ssh

stdin, stdout, stderr = ssh.exec_command('mkdir TestDir') # creating directory
stdin, stdout, stderr = ssh.exec_command('ls') #listing directory
print(stdout)
print(stdout.read())