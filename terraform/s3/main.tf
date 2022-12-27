module "kms" {
  source  = "app.terraform.io/thkim0022/kms/aws"
  version = "1.0.3"

  deletion_window_in_days = var.kms_deletion_window_in_days
  alias_name              = var.s3_bucket_name

  tags = var.tags
}

module "s3" {
  source  = "app.terraform.io/thkim0022/s3/aws"
  version = "1.0.1"

  bucket_name = var.s3_bucket_name
  kms_key_id     = module.kms.key_id
  kms_alias_id   = module.kms.alias_id

  tags = var.tags
}