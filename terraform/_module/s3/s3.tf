resource "aws_s3_bucket" "this" {
  bucket = var.bucket_name

  tags = merge(
    var.tags,
    {
      "Name": var.bucket_name,
      "Type": "s3"
    }
  )
}