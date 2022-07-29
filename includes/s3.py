import os, boto3
s3_access, s3_secret, s3_bucket = os.getenv("S3_ACCESS"), os.getenv("S3_SECRET"), os.getenv("S3_BUCKET")
def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client("s3", aws_access_key_id=s3_access, aws_secret_access_key=s3_secret)
    try:
        s3.upload_file(local_file, bucket, s3_file, ExtraArgs={"ACL": "public-read"})
        print("upload successful")
        return True
    except FileNotFoundError:
        print("file was not found")
        return False
    except NoCredentialsError:
        print("credentials not available")
        return False