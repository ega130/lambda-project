import boto3
import time

# LocalStackのエンドポイントを指定
localstack_endpoint = 'http://localhost:4566'

# Lambdaクライアントを作成
lambda_client = boto3.client('lambda', endpoint_url=localstack_endpoint, region_name='us-east-1')

function_name = 'sample_lambda'

# 関数がすでに存在するかどうかを確認
try:
    lambda_client.get_function(FunctionName=function_name)
    function_exists = True
except lambda_client.exceptions.ResourceNotFoundException:
    function_exists = False

# 関数が存在する場合は更新、存在しない場合は作成
if function_exists:
    response = lambda_client.update_function_code(
        FunctionName=function_name,
        ZipFile=open('lambda_function.zip', 'rb').read(),
    )
else:
    response = lambda_client.create_function(
        FunctionName=function_name,
        Runtime='python3.8',
        Role='arn:aws:iam::000000000000:role/lambda-role',
        Handler='lambda_function.lambda_handler',
        Code={'ZipFile': open('lambda_function.zip', 'rb').read()},
    )

# Lambda関数がActive状態になるまで待機
while True:
    response = lambda_client.get_function(FunctionName=function_name)
    if response['Configuration']['State'] == 'Active':
        break
    time.sleep(1)
