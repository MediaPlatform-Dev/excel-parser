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

resource "aws_iam_policy" "this" {
  name = "iam-policy-${var.lambda_function_name}"

  policy = jsonencode(
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "kms:Decrypt",
            "kms:GenerateDataKey",
            "s3:ListBucket",
            "s3:GetObject",
            "s3:GetObjectVersion",
            "s3:CopyObject",
            "s3:HeadObject"
          ],
          "Resource": [
            "arn:aws:s3:::${var.lambda_function_name}",
            "arn:aws:s3:::${var.lambda_function_name}/*"
          ]
        }
      ]
    }
  )

  depends_on = [
    aws_iam_role.this
  ]

  tags = merge(
    var.tags,
    {
      "Name": "iam-policy-${var.lambda_function_name}",
      "Type": "policy"
    }
  )
}

resource "aws_iam_role_policy_attachment" "this" {
  role       = aws_iam_role.this.id
  policy_arn = aws_iam_policy.this.arn

  depends_on = [
    aws_iam_policy.this
  ]
}