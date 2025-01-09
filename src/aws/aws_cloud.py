import boto3
from botocore.exceptions import NoCredentialsError, ClientError


class AWSHandler:
    """
    A wrapper class to interact with AWS services such as S3 and DynamoDB.
    """

    def __init__(self, region_name="us-east-1"):
        """
        Initializes the AWS SDK instance.

        Args:
            region_name (str): The AWS region to use. Default is 'us-east-1'.
        """
        self.region_name = region_name
        self.s3 = boto3.client("s3", region_name=self.region_name)
        self.dynamodb = boto3.resource("dynamodb", region_name=self.region_name)

    def create_s3_bucket(self, bucket_name):
        """
        Creates an S3 bucket in the specified region.

        Args:
            bucket_name (str): The name of the bucket to create.

        Returns:
            bool: True if the bucket was created successfully, False otherwise.
        """
        try:
            if self.region_name == "us-east-1":
                self.s3.create_bucket(Bucket=bucket_name)
            else:
                self.s3.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={"LocationConstraint": self.region_name},
                )
            print(f"S3 bucket '{bucket_name}' created successfully.")
            return True
        except ClientError as e:
            print(f"An error occurred: {str(e)}")
            return False

    def upload_to_s3(self, bucket_name, file_path, key):
        """
        Uploads a file to an S3 bucket.

        Args:
            bucket_name (str): The name of the bucket.
            file_path (str): The local path of the file to upload.
            key (str): The S3 object key for the uploaded file.

        Returns:
            None
        """
        try:
            self.s3.upload_file(file_path, bucket_name, key)
            print(f"File uploaded to S3: {bucket_name}/{key}")
        except NoCredentialsError:
            print("AWS credentials not found.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def upload_string_to_s3(self, bucket_name, key, content):
        """
        Uploads a string as an object to an S3 bucket.

        Args:
            bucket_name (str): The name of the bucket.
            key (str): The S3 object key for the uploaded content.
            content (str): The string content to upload.

        Returns:
            None
        """
        try:
            self.s3.put_object(Bucket=bucket_name, Key=key, Body=content)
            print(f"String uploaded to S3: {bucket_name}/{key}")
        except NoCredentialsError:
            print("AWS credentials not found.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def download_from_s3(self, bucket_name, key, download_path):
        """
        Downloads a file from an S3 bucket.

        Args:
            bucket_name (str): The name of the bucket.
            key (str): The S3 object key of the file to download.
            download_path (str): The local path to save the downloaded file.

        Returns:
            None
        """
        try:
            self.s3.download_file(bucket_name, key, download_path)
            print(f"File downloaded from S3: {bucket_name}/{key}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def list_s3_objects(self, bucket_name):
        """
        Lists the objects in an S3 bucket.

        Args:
            bucket_name (str): The name of the bucket.

        Returns:
            list: A list of objects in the bucket, or an empty list if none are found.
        """
        try:
            response = self.s3.list_objects_v2(Bucket=bucket_name)
            return response.get("Contents", [])
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return []
