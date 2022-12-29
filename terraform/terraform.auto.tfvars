# General
region = "ap-northeast-2"

# IAM
iam_policy = [
  "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
  "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
]

# Lambda
function_name = "excel-to-mysql"
handler = "lambda_function.lambda_handler"
runtime = "python3.9"
timeout = "60"

# Tags
tags = {
  "Dept": "media-platform"
}