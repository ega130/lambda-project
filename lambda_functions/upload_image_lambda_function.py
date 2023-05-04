import boto3
import base64

def lambda_handler(event, context):
    s3_client = boto3.client('s3', endpoint_url='http://localstack:4566', region_name='us-east-1')

    # イベントデータからPNG画像のパスを取得
    png_image_base64 = event.get('png_image_base64')

    # 画像をbase64デコードしてバイトデータに変換
    png_image_data = base64.b64decode(png_image_base64)

    # S3バケットにPNG画像をアップロード
    s3_client.put_object(Bucket='my-upload-bucket', Key='uploaded_image.png', Body=png_image_data)

    # 処理が成功した場合、成功メッセージを返す
    return {
        'statusCode': 200,
        'body': 'Image uploaded to S3 successfully.'
    }
