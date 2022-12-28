resource "aws_kms_key" "this" {
   description             = "Encryption Key for the S3 Bucket"
   deletion_window_in_days = var.deletion_window_in_days

   tags = merge(
     var.tags,
     {
       "Name": "kms-${var.alias_name}",
       "Type": "kms"
     }
   )
 }

 resource "aws_kms_alias" "this" {
   name          = "alias/${lower(var.alias_name)}"
   target_key_id = aws_kms_key.this.key_id

   depends_on = [
     aws_kms_key.this
   ]
 }