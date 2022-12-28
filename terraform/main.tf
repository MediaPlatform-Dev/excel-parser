module "iam" {
  source = "./_module/iam"

  lambda_function_name = var.function_name

  tags = var.tags
}

module "s3" {
  source  = "./_module/s3"

  bucket_name = var.function_name
  lambda_function_arn = module.lambda.arn

  tags = var.tags
}

module "lambda" {
  source  = "./_module/lambda"

  function_name  = var.function_name
  iam_role_arn = module.iam.arn
  handler = var.handler
  runtime = var.runtime
  timeout = var.timeout
  s3_bucket_arn = module.s3.arn

  tags = var.tags
}