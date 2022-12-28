# General
region = "ap-northeast-2"

# kms
deletion_window_in_days = 7

# Lambda
function_name = "excel-parser"
handler = "lambda_function.lambda_handler"
runtime = "python3.9"

# Tags
tags = {
  "Dept": "media-platform"
}