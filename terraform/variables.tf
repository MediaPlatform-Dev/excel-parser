variable "region" {
  description = "AWS region"
  type        = string
}

variable "iam_policy" {}
variable "function_name" {}
variable "handler" {}
variable "runtime" {}
variable "timeout" {}

variable "tags" {}