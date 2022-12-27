module "lambda" {
  source  = "app.terraform.io/thkim0022/lambda/aws"
  version = "1.0.0"

  function_name  = var.lambda_function_name
  s3_bucket_name = var.s3_bucket_name

  tags = var.tags
}