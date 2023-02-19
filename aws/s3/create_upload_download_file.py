import os
import logging
import boto3
from botocore.exceptions import ClientError


"""Create an S3 bucket in a specified region
    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """
def create_bucket(bucket_name, region=None):
    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True


"""Upload a file to an S3 bucket
    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
def upload_file(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


# Retrieve the list of existing buckets
def show_buckets(region="us-east-1"):
    s3 = boto3.client('s3', region)
    response = s3.list_buckets()
    # Output the bucket names
    print('Existing buckets:')
    for bucket in response['Buckets']:
        print(f'  {bucket["Name"]}')


def download_file(bucket, object_name, file_name):
    s3 = boto3.client('s3')
    s3.download_file(bucket, object_name, file_name)


def test():
    create_bucket("sondosbucketH")  # it should return with an error
    upload_file("/home/osboxes/tsofen-course/aws/s3/vpc.yml", "sondosbucket222")
    download_file("sondosbucket222", "vpc.yml", "/home/osboxes/tsofen-course/aws/s3/vpc2.yml")
    show_buckets()


test()