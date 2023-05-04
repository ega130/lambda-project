import boto3

# LocalStackのエンドポイントを指定
localstack_endpoint = 'http://localhost:4566'

# Lambdaクライアントを作成
# このクライアントは、LocalStackを使用してLambda関数を実行するために使用されます。
lambda_client = boto3.client('lambda', endpoint_url=localstack_endpoint, region_name='us-east-1')

# Lambda関数を実行
# LocalStackは、Lambda関数の実行イベントを受信し、新しい環境を開始します。
# Dockerコンテナ用のサービスエンドポイントが作成され、関数が実行されるエグゼキュータに割り当てられます。
# Lambda関数用のDockerコンテナが作成され、設定が適用されます。
# Lambda関数を実行するために必要なランタイムおよび依存関係がインストールされます。
response = lambda_client.invoke(FunctionName='sample_lambda')

# 実行が終了すると、invoke_lambda.py スクリプトの実行結果が出力されます。
# これにより、AWS Lambda関数が正しく実行されたことが確認できます。
output = response['Payload'].read().decode('utf-8')
print("Lambda output:", output)
