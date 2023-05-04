import boto3
import json

# 標準入力からfirst_nameとlast_nameを取得
first_name = input("Enter first name: ")
last_name = input("Enter last name: ")

# eventディクショナリを作成
event = {
    "first_name": first_name,
    "last_name": last_name
}

# LocalStackのエンドポイントを指定
localstack_endpoint = 'http://localhost:4566'

# Lambdaクライアントを作成
# このクライアントは、LocalStackを使用してLambda関数を実行するために使用されます。
lambda_client = boto3.client('lambda', endpoint_url=localstack_endpoint, region_name='us-east-1')

# Lambda関数を実行してeventディクショナリを渡す
# LocalStackは、Lambda関数の実行イベントを受信し、新しい環境を開始します。
# Dockerコンテナ用のサービスエンドポイントが作成され、関数が実行されるエグゼキュータに割り当てられます。
# Lambda関数用のDockerコンテナが作成され、設定が適用されます。
# Lambda関数を実行するために必要なランタイムおよび依存関係がインストールされます。
response = lambda_client.invoke(
    FunctionName='sample_lambda',
    Payload=json.dumps(event)  # eventディクショナリをJSONに変換してPayload引数に渡す
)

# 実行が終了すると、invoke_lambda.py スクリプトの実行結果が出力されます。
# これにより、AWS Lambda関数が正しく実行されたことが確認できます。
output = response['Payload'].read().decode('utf-8')
print("Lambda output:", output)
