import boto3

# LocalStackのエンドポイントを指定
localstack_endpoint = 'http://localhost:4566'

# Lambdaクライアントを作成
lambda_client = boto3.client('lambda', endpoint_url=localstack_endpoint, region_name='us-east-1')

# Lambda関数を実行
response = lambda_client.invoke(FunctionName='sample_lambda')
output = response['Payload'].read().decode('utf-8')
print("Lambda output:", output)
