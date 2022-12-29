resource "aws_cloudwatch_log_group" "this" {
  name              = "/aws/lambda/${var.lambda_function_name}"
  retention_in_days = 1

  tags = merge(
    var.tags,
    {
      "Name": "cloudwatch-log-group-${var.lambda_function_name}",
      "Type": "log_group"
    }
  )
}