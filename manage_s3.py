"""
@author Bryan Hopkins pennbwh@gmail.com

This script provides some helper functionality to add and manage files from an S3 bucket.
This exists largely as a practical training exercise and conceptual example.

"""

import boto3
from botocore.client import ClientError

# https://boto3.readthedocs.io/en/latest/reference/services/s3.html
s3client = boto3.client("s3")
gitlab_bucket_name = "VAULT_S3_BUCKET_NAME"
try:
    s3client.head_bucket(Bucket=gitlab_bucket_name)
    print("Bucket %s exists" % gitlab_bucket_name)
except ClientError:
    print("Bucket %s doesn't exist, creating" % gitlab_bucket_name)
    s3client.create_bucket(ACL="private", Bucket=gitlab_bucket_name)


def s3_store_repo(object_name, backup_file):
    s3client.upload_fileobj(backup_file, gitlab_bucket_name, object_name)


def s3_object_name_from_repo(project_name, branch_name):
    return project_name + "-" + branch_name + ".tar.gz"


def s3_object_last_modified(object_name):
    object = boto3.resource("s3").Object(gitlab_bucket_name, object_name)
    try:
        return object.last_modified
    except ClientError:
        return None
