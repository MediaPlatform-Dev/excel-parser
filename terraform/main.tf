module "kms" {
  source  = "_module/kms"

  deletion_window_in_days = var.deletion_window_in_days
  alias_name              = var.function_name

  tags = var.tags
}

module "s3" {
  source  = "_module/s3"

  bucket_name = var.function_name
  kms_key_id  = module.kms.key_id

  tags = var.tags
}

module "lambda" {
  source  = "_module/lambda"

  function_name  = var.function_name
  handler = var.handler
  runtime = var.runtime

  tags = var.tags
}