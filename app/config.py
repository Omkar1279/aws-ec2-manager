import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from decouple import config


def get_ec2_client():
    try:
        return boto3.client('ec2',
                            aws_access_key_id='ACCESS_KEY',
                            aws_secret_access_key='SECRET_KEY',
                            region_name='REGION')
    except (NoCredentialsError, PartialCredentialsError):
        raise Exception("AWS credentials are not properly configured.")
