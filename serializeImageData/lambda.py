import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3 (called by Step Functions)"""

    # Pull bucket & key from the Step Function input
    bucket = event["s3_bucket"]
    key    = event["s3_key"]

    # Download the image from S3 into Lambda's /tmp directory
    download_path = "/tmp/image.png"
    s3.download_file(bucket, key, download_path)

    # Read and base64-encode the file contents
    with open(download_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    # Return payload back to the Step Function
    return {
        "statusCode": 200,
        "body": {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }

