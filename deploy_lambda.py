import boto3
import time

# LocalStackのエンドポイントを指定
localstack_endpoint = 'http://localhost:4566'

# Lambdaクライアントを作成
lambda_client = boto3.client('lambda', endpoint_url=localstack_endpoint, region_name='us-east-1')

# Lambda関数をデプロイ
response = lambda_client.create_function(
    FunctionName='sample_lambda',
    Runtime='python3.8',
    Role='arn:aws:iam::000000000000:role/lambda-role',
    Handler='lambda_function.lambda_handler',
    Code={'ZipFile': open('lambda_function.zip', 'rb').read()},
)

# Lambda関数がActive状態になるまで待機
while True:
    response = lambda_client.get_function(FunctionName='sample_lambda')
    if response['Configuration']['State'] == 'Active':
        break
    time.sleep(1)
