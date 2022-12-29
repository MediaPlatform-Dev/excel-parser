resource "aws_iam_role" "this" {
  name = var.name

  assume_role_policy = jsonencode(
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Action": "sts:AssumeRole",
          "Principal": {
            "Service": "lambda.amazonaws.com"
          },
          "Effect": "Allow"
        }
      ]
    }
  )

  managed_policy_arns = var.policy_arns

  tags = merge(
    var.tags,
    {
      "Name": var.name,
      "Type": "role"
    }
  )
}