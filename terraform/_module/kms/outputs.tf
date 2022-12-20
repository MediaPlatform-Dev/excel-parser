output "kms_key_id" {
  value = aws_kms_key.this.key_id
}

output "kms_alias_id" {
  value = aws_kms_alias.this.id
}

output "kms_alias_name" {
  value = aws_kms_alias.this.name
}