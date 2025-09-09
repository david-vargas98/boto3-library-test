import boto3

ec2 = boto3.resource('ec2')

# creating an ec2 instance
print("Creating the instance, wait...")
instance = ec2.create_instances(
    MinCount=1,
    MaxCount=1,
    InstanceType='t3.micro',
    ImageId='ami-0fd3ac4abb734302a' # LOOK THIS UP - CONSOLE
)
print("The instance was created")

# listing instances
instances_list = list(ec2.instances.all())
for instance in instances_list:
    print(instance)

# getting instance details by using the client
client = boto3.client('ec2')

instance_description = client.describe_instances(InstanceIds=['i-0e32796b4a4eba5fd'])

print(instance_description['Reservations'][0]['Instances'][0]['State'])

# stopping an instance
print("Stopping the instance...")
stop_instance = client.stop_instances(InstanceIds=['i-0e32796b4a4eba5fd'])
print(stop_instance)

# starting an instance
start_instance = client.start_instances(InstanceIds=['i-0e32796b4a4eba5fd'])
print("\nStarting the instance...")
print(start_instance)

#Terminate (delete) an instance
print("Terminating the instance...")
terminated = client.terminate_instances(InstanceIds=['i-0e32796b4a4eba5fd'])
print(terminated)