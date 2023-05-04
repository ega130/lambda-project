import boto3
import json
import os
from PIL import Image
from io import BytesIO

s3_client = boto3.client('s3', endpoint_url='http://localstack:4566', region_name='us-east-1')

def lambda_handler(event, context):
    # SQSメッセージからS3イベントを取得
    s3_event = json.loads(event['Records'][0]['body'])

    # S3オブジェクトの情報を取得
    bucket = s3_event['Records'][0]['s3']['bucket']['name']
    key = s3_event['Records'][0]['s3']['object']['key']

    # 入力画像をダウンロード
    response = s3_client.get_object(Bucket=bucket, Key=key)
    input_image = Image.open(BytesIO(response['Body'].read()))

    # 画像をJPEG形式に変換
    output_image = BytesIO()
    input_image.convert('RGB').save(output_image, 'JPEG')

    # 変換した画像を保存用バケットにアップロード
    save_bucket = 'my-save-bucket'
    save_key = os.path.splitext(key)[0] + '.jpeg'
    s3_client.put_object(Bucket=save_bucket, Key=save_key, Body=output_image.getvalue())

    return {
        'statusCode': 200,
        'body': json.dumps('Image converted and saved successfully!')
    }
