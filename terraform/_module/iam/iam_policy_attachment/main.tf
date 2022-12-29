resource "aws_iam_policy_attachment" "this" {
  name       = "iam-policy-attachment-${var.policy_name}"
  roles      = [var.role_name]
  policy_arn = var.policy_arn
}