import boto3
import json
import os

BUCKET_NAME = 'my-s3-bucket'
WEBSITE_BUCKET_NAME = 'website-host-bucket'


def s3_client():
    s3 = boto3.client('s3')
    """ :type : pybpto3.s3"""
    return s3


def create_bucket(bucket_name):
    return s3_client().create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': 'ap-south-1'
        }
    )


def create_bucket_policy():
    bucket_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AddPerm",
                "Effect": "Allow",
                "Principal": "*",
                "Action": ["s3:*"],
                "Resource": ["arn:aws:s3:::my-s3-bucket/*"]
            }
        ]
    }

    policy_strings = json.dumps(bucket_policy)
    print(policy_strings)

    return s3_client().put_bucket_policy(
        Bucket=BUCKET_NAME,
        Policy=policy_strings
    )


def list_bucket():
    return s3_client().list_buckets()


def get_bucket_policy():
    return s3_client().get_bucket_policy(Bucket=BUCKET_NAME)


def get_bucket_encryption():
    return s3_client().get_bucket_encryption(Bucket=BUCKET_NAME)


def update_bucket_policy(bucket_name):
    bucket_policy = {
        'Version': '2012-10-17',
        'Statement': [
            {
                'Sid': 'AddPerm',
                'Effect': 'Allow',
                'Principal': '*',
                'Action': [
                    's3:DeleteObject',
                    's3:GetObject',
                    's3:PutObject'
                ],
                'Resource': 'arn:aws:s3:::' + bucket_name + '/*'
            }
        ]
    }

    policy_string = json.dumps(bucket_policy)

    return s3_client().put_bucket_policy(
        # Bucket=BUCKET_NAME,
        Bucket=WEBSITE_BUCKET_NAME,
        Policy=policy_string
    )


def server_side_encryption():
    return s3_client().put_bucket_encryption(
        Bucket=BUCKET_NAME,
        ServerSideEncryptionConfiguration={
            'Rules': [
                {
                    'ApplyServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'AES256'
                    }
                }
            ]
        }
    )


def delete_bucket():
    return s3_client().delete_bucket(Bucket=BUCKET_NAME)


def upload_small_file():
    file_path = os.path.dirname(__file__) + '/smallfile'
    return s3_client().upload_file(file_path, BUCKET_NAME, 'smallfile.txt')


def read_object_from_bucket():
    object_key = 'smallfile.txt'
    return s3_client().get_object(Bucket=BUCKET_NAME, Key=object_key)


def version_bucket_file():
    s3_client().put_bucket_versioning(
        Bucket=BUCKET_NAME,
        VersioningConfiguration={
            'Status': 'Enabled'
        }
    )


def upload_new_version_object():
    file_path = os.path.dirname(__file__) + '/smallfile'
    return s3_client().upload_file(file_path, BUCKET_NAME, 'smallfile.txt')


def put_lifecycle_policy():
    lifecycle_policy = {
        "Rules": [
            {
                "ID": "Move smallfile to Glacier",
                "Prefix": "smallfile",
                "Status": "Enabled",
                "Transitions": [
                    {
                        "Date": "2020-11-24T00:00:00.000Z",
                        "StorageClass": "GLACIER"
                    }
                ]
            },
            {
                "Status": "Enabled",
                "Prefix": "",
                "NoncurrentVersionTransitions": [
                    {
                        "NoncurrentDays": 2,
                        "StorageClass": "GLACIER"
                    }
                ],
                "ID": "Move old version to Glacier"
            }
        ]
    }

    s3_client().put_bucket_lifecycle_configuration(
        Bucket=BUCKET_NAME,
        LifecycleConfiguration=lifecycle_policy
    )


def host_static_website():
    s3 = boto3.client('s3', region_name='ap-south--1')

    s3.create_bucket(
        Bucket=WEBSITE_BUCKET_NAME,
        CreateBucketConfiguration={
            'LocationConstraint': 'ap-south-1'
        }
    )

    update_bucket_policy(WEBSITE_BUCKET_NAME)

    website_configuration = {
        'ErrorDocument': {'Key': 'error.html'},
        'IndexDocument': {'Suffix': 'index.html'}
    }

    s3_client().put_bucket_website(
        Bucket=WEBSITE_BUCKET_NAME,
        WebsiteConfiguration=website_configuration
    )

    index_file = os.path.dirname(__file__) + '/index.html'
    error_file = os.path.dirname(__file__) + '/error.html'
    
    s3_client().put_object(Bucket=WEBSITE_BUCKET_NAME, ACL='public-read', Key='index.html',
                           Body=open(index_file).read(), ContentType='text/html')
    s3_client().put_object(Bucket=WEBSITE_BUCKET_NAME, ACL='public-read', Key='error.html',
                           Body=open(error_file).read(), ContentType='text/html')


if __name__ == '__main__':
    # create_bucket(BUCKET_NAME)
    # print(create_bucket_policy())
    # print(list_bucket())
    # get_bucket_policy()
    # get_bucket_encryption()
    # update_bucket_policy(BUCKET_NAME)
    # server_side_encryption()
    # delete_bucket()
    # upload_small_file()
    # read_object_from_bucket()
    # version_bucket_file()
    # upload_new_version_object()
    # put_lifecycle_policy()
    host_static_website()