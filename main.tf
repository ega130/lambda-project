provider "aws" {
  profile                     = "localstack"
  region                      = "us-east-1"
  access_key                  = "test"
  secret_key                  = "test"
  s3_use_path_style           = true
  skip_credentials_validation = true
  skip_requesting_account_id  = true

  endpoints {
    s3     = "http://localhost:4566"
    sqs    = "http://localhost:4566"
    lambda = "http://localhost:4566"
  }
}

resource "aws_s3_bucket" "upload_bucket" {
  bucket = "my-upload-bucket"
}

resource "aws_s3_bucket" "save_bucket" {
  bucket = "my-save-bucket"
}

resource "aws_sqs_queue" "s3_event_queue" {
  name = "s3-event-queue"
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.upload_bucket.id

  queue {
    queue_arn     = aws_sqs_queue.s3_event_queue.arn
    events        = ["s3:ObjectCreated:*"]
    filter_suffix = ".png"
  }
}

resource "aws_iam_role" "lambda_role" {
  name = "sample_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_lambda_function" "full_name_lambda" {
  function_name = "full_name_lambda"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"

  role = aws_iam_role.lambda_role.arn

  filename = "full_name_lambda_function.zip"
}


resource "aws_lambda_function" "image_conversion_lambda" {
  function_name = "image_conversion_lambda"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"

  role = aws_iam_role.lambda_role.arn

  filename = "image_conversion_lambda_function.zip"
}

resource "aws_lambda_event_source_mapping" "sqs_lambda_mapping" {
  event_source_arn = aws_sqs_queue.s3_event_queue.arn
  function_name    = aws_lambda_function.image_conversion_lambda.arn
}
