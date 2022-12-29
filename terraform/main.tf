module "iam_role" {
  source = "./_module/iam/role"

  name = "iam-role-${var.function_name}"
  policy_arns = var.iam_policy
  tags = var.tags
}

#module "attachment" {
#  source = "./_module/iam/attachment"
#
#  role_name = module.role.name
#
#  for_each    = var.iam_policy
#  policy_name = each.key
#  policy_arn  = each.value
#}

module "s3" {
  source  = "./_module/s3/bucket"

  bucket_name         = var.function_name
  lambda_function_arn = module.lambda.arn

  tags = var.tags
}

module "lambda" {
  source  = "./_module/lambda/function"

  function_name  = var.function_name
  iam_role_arn   = module.iam_role.arn
  handler        = var.handler
  runtime        = var.runtime
  timeout        = var.timeout
  s3_bucket_arn  = module.s3.arn

  tags = var.tags
}

module "cloudwatch" {
  source = "./_module/cloudwatch/log_group"

  lambda_function_name = var.function_name

  tags = var.tags
}