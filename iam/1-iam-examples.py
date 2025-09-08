import boto3
from botocore.exceptions import ClientError

iam_client = boto3.client('iam')

# list all of the users
print("\tAll of the users")
try:
    iam_dict_users = iam_client.list_users()

    for user in iam_dict_users['Users']:
        print(f"- {user['UserName']}")
except ClientError as e:
    print(f"Error: {e}")
    
# list all of the groups
print("\n\tAll of the groups")
try:
    iam_dict_groups = iam_client.list_groups()

    for group in iam_dict_groups['Groups']:
        print(f"- {group['GroupName']}")
except ClientError as e:
    print(f"Error: {e}")

# create a user
print("\n\tCreate user")
try:
    user_name_create = 'Test-user-boto3'
    response = iam_client.create_user(UserName=user_name_create)
    print(response)
except ClientError as e:
    if e.response['Error']['Code'] == 'EntityAlreadyExists':
        print(f"The user '{user_name_create}' already exists. Skipping creation.")
    else:
        print(f"Error: {e}")

# add user to group
print("\n\tAdd a user to a group")
try:
    user_name_to_add = 'Test-user-boto3'
    group_name_to_add = 'full-permission'

    response =  iam_client.add_user_to_group(GroupName=group_name_to_add, UserName=user_name_to_add)
    
    print(f"The user '{user_name_to_add}' was added to '{group_name_to_add}' group.")
except ClientError as e:
    if e.response['Error']['Code'] == 'NoSuchEntity':
        print(f"Error: User '{user_name_to_add}' or group '{group_name_to_add}' does not exist.")
    elif e.response['Error']['Code'] == 'LimitExceeded':
        print(f"Error: The user is already in the maximum number of groups.")
    else:
        print(f"Error adding user to group: {e}")

# delete a user from a group
print("\n\tDelete a user from a group")

user_name_to_delete = 'Test-user-boto3'
try:
    iam_users = iam_client.list_users()
    print(f"Checking groups for user '{user_name_to_delete}'...\n")

    user_groups = iam_client.list_groups_for_user(UserName=user_name_to_delete)

    if user_groups['Groups']:
        print(f"The user '{user_name_to_delete}' belongs to the following groups:")
        for group in user_groups['Groups']:
            print(f"- {group['GroupName']}")

        print("\nRemoving user from groups...\n")
        for group in user_groups['Groups']:
            group_name = group['GroupName']
            response = iam_client.remove_user_from_group(GroupName=group_name, UserName=user_name_to_delete)
            print(f"The user '{user_name_to_delete}' was successfully removed from the '{group_name}' group.")
    else:
        print(f"The user '{user_name_to_delete}' is not in any groups.")

    iam_client.delete_user(UserName=user_name_to_delete)
    print(f"\nRemoving user...\nThe '{user_name_to_delete}' user was successfully deleted.")
except ClientError as e:
    print(f"Error: {e}")