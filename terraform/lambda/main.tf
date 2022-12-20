module "lambda" {
  source = "../_module/lambda"

  lambda_function_name = var.lambda_function_name
  s3_bucket_name       = var.s3_bucket_name

  tags = var.tags
}