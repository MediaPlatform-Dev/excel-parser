variable "region" {
  description = "AWS region"
  type        = string
}

variable "deletion_window_in_days" {}
variable "function_name" {}
variable "handler" {}
variable "runtime" {}

variable "tags" {}