package scalenyx.s3

test_public_bucket_denied if {
    msg := deny[_] with input as {"resource": {"aws_s3_bucket": {"public": true}}}
    msg == "Public S3 buckets are not allowed"
}

test_private_bucket_allowed if {
    deny_empty := deny with input as {"resource": {"aws_s3_bucket": {"public": false}}}
    count(deny_empty) == 0
}
