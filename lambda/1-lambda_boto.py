import boto3

# taking the actual code from the file
actual_lambda_func = "1-hello-world.py"

with open(actual_lambda_func, 'r') as file:
    function_code = file.read()

print(function_code)

# defining needed variables
function_name = "Helloworld2"
runtime = 'python3.12'
handler = 'lambda_function.lambda_handler'

# defining an IAM role which will be used by the lambda function to be executed
import json

iam_client = boto3.client('iam', region_name='us-east-1')

# iam policy for lambda function to write logs in cloudwatch
lambda_execution_policy = {
    'Version': '2012-10-17',
    'Statement':[
        {
            'Effect':'Allow',
            'Action':[
                'logs:CreateLogGroup',
                'logs:CreateLogStream',
                'logs:PutLogEvents'
            ],
            'Resource':'arn:aws:logs:*:*:*'
        }
    ]
}

# # role name
role_name = 'LambdaExecutionRole'

# creation of role response
role_response = iam_client.create_role(
    RoleName= role_name,
    AssumeRolePolicyDocument= json.dumps( # CRITICAL: Trust policy - it says WHO or WHAT service can assume/use this role 
        {
            'Version':'2012-10-17',
            'Statement':[
                {
                    'Effect':'Allow',
                    'Principal':{
                        'Service':'lambda.amazonaws.com' # it means aws lambda service is the only entity which is allowed to use this role
                    },
                    'Action':'sts:AssumeRole' # allows 'lambda.amazonaws.com' to perform the 'sts:AssumeRole' action, i.e. to take the permissions from this role 
                }
            ]
        }
    )
)

# policy name
policy_name = 'LambdaExecutionPolicy'

iam_client.put_role_policy(
    RoleName= role_name,
    PolicyName= policy_name,
    PolicyDocument= json.dumps(lambda_execution_policy)
)

# after role creation, an ARN is assigned and we get it
role_arn = role_response['Role']['Arn']
print(role_arn)
role_arn = 'arn:aws:iam::114914321936:role/LambdaExecutionRole'

# ------------------ lambda function creation
import zipfile
import io

lambda_client = boto3.client('lambda', region_name='us-east-1')

with io.BytesIO() as deployment_package: # deployment_package is a temp in-memory temp file
    with zipfile.ZipFile(deployment_package, 'w') as zipFile: # opening deployment_package as a zip file in write mode
        zipFile.writestr('lambda_function.py', function_code) # writing the code from the lambda function to the zip file

    create_function_response =lambda_client.create_function(
        FunctionName= function_name,
        Runtime= runtime,
        Role= role_arn,
        Handler= handler,
        Code={'ZipFile': deployment_package.getvalue()}
    )

# invoking function
invoke_response = lambda_client.invoke(
    FunctionName= function_name
)

payload = invoke_response['Payload'].read() # extracts the payload (lambda function response), it's a stream object, so it needs to be read

payload.decode('utf-8') # decodes the payload from bytes to string using utf-8 encoding

print(payload) # prints the payload

# deletes the lambda function
lambda_client.delete_function(
    FunctionName= function_name
)