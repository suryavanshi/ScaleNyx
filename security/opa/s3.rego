package scalenyx.s3

deny contains msg if {
  input.resource.aws_s3_bucket.public
  msg := "Public S3 buckets are not allowed"
}
