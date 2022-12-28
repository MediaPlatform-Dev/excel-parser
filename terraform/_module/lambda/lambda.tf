resource "aws_lambda_function" "this" {
  function_name = var.function_name
  role          = var.iam_role_arn

  handler = var.handler
  runtime = var.runtime

  filename = "${var.function_name}.zip"
  source_code_hash = filebase64sha256("${var.function_name}.zip")

  tags = merge(
    var.tags,
    {
      "Name": var.function_name,
      "Type": "lambda"
    }
  )
}