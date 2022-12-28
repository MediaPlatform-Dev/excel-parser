resource "aws_iam_role" "this" {
  name = "iam-role-${var.function_name}"

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

  tags = merge(
    var.tags,
    {
      "Name": "iam-role-${var.function_name}",
      "Type": "role"
    }
  )
}