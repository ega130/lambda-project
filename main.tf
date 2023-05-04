provider "aws" {
  region                      = "us-east-1"
  access_key                  = "dummy"
  secret_key                  = "dummy"
  s3_force_path_style         = true
  skip_credentials_validation = true
  skip_requesting_account_id  = true

  endpoints {
    lambda = "http://localhost:4566"
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

resource "aws_lambda_function" "sample_lambda" {
  function_name = "sample_lambda"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"

  role = aws_iam_role.lambda_role.arn

  filename = "path/to/your/lambda_function.zip"
}
