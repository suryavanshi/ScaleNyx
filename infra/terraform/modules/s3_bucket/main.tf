terraform {
  required_version = ">= 1.5.0"
}

resource "aws_s3_bucket" "this" {
  bucket = var.bucket_name
  acl    = "private"

  tags = var.tags
}

resource "aws_s3_bucket_server_side_encryption_configuration" "default" {
  bucket = aws_s3_bucket.this.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
