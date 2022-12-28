output "key_id" {
  value = aws_kms_key.this.key_id
}

output "alias_id" {
  value = aws_kms_alias.this.id
}

output "alias_name" {
  value = aws_kms_alias.this.name
}