resource "aws_iam_role" "this" {
  name = "iam-role-${var.lambda_function_name}"

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
      "Name": "iam-role-${var.lambda_function_name}",
      "Type": "role"
    }
  )
}

resource "aws_iam_policy_attachment" "this" {
  name       = "iam-policy-attachment-${data.aws_iam_policy.AWSLambdaBasicExecutionRole.name}"
  roles      = [aws_iam_role.this.name]
  policy_arn = data.aws_iam_policy.AWSLambdaBasicExecutionRole.arn
}