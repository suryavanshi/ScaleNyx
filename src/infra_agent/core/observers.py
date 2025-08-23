import boto3


def verify_s3_bucket(name: str) -> bool:
    """Check if the given S3 bucket exists."""
    s3 = boto3.client("s3")
    try:
        s3.head_bucket(Bucket=name)
        return True
    except Exception:
        return False
