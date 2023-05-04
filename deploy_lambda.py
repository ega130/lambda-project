import boto3
import time
import zipfile

# lambda_function.pyをZIPファイルに圧縮
def create_zip_file(zip_name, file_name):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file_name)

zip_file_name = 'lambda_function.zip'
create_zip_file(zip_file_name, 'lambda_function.py')

# LocalStackのエンドポイントを指定
localstack_endpoint = 'http://localhost:4566'

# Lambdaクライアントを作成 (LocalStackがAWS Lambdaサービスのエミュレーションを開始)
lambda_client = boto3.client('lambda', endpoint_url=localstack_endpoint, region_name='us-east-1')

function_name = 'sample_lambda'

# 関数がすでに存在するかどうかを確認 (lambda.GetFunctionリクエストが送信され、関数が存在しないことが確認されます)
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
    # Lambda関数が作成されます (lambda.CreateFunctionリクエストが送信され、新しいLambda関数が作成されます)
    response = lambda_client.create_function(
        FunctionName=function_name,
        Runtime='python3.8',
        Role='arn:aws:iam::000000000000:role/lambda-role', # sts.AssumeRoleリクエストが送信され、ロールの権限が取得されます
        Handler='lambda_function.lambda_handler',
        Code={'ZipFile': open('lambda_function.zip', 'rb').read()}, # s3.CreateBucketリクエストが送信され、内部的にS3バケットが作成されます。s3.PutObjectリクエストが送信され、Lambda関数のコードがS3バケットに保存されます
    )

# Lambda関数がActive状態になるまで待機 (Lambda関数のコードがディスクに保存され、Dockerイメージがプルされます。Lambda関数がアクティブ状態になります)
while True:
    response = lambda_client.get_function(FunctionName=function_name)
    if response['Configuration']['State'] == 'Active':
        break
    time.sleep(1)
