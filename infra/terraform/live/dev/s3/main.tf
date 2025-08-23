terraform {
  required_version = ">= 1.5.0"
}

provider "aws" {
  region                      = "us-east-1"
  skip_credentials_validation = true
  skip_requesting_account_id  = true
}

module "bucket" {
  source      = "../../modules/s3_bucket"
  bucket_name = var.bucket_name
  tags        = var.tags
}

variable "bucket_name" {
  type = string
}

variable "tags" {
  type = map(string)
  default = {
    environment = "dev"
  }
}

output "bucket_id" {
  value = module.bucket.bucket_id
}
