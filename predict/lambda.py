import json
import boto3
import base64

# Name of your deployed endpoint
ENDPOINT = "image-classification-udemy-danut-01"
runtime = boto3.client("sagemaker-runtime")

def lambda_handler(event, context):
    # 1. If SFN wrapped your payload in `body`, parse it
    if "body" in event:
        payload = json.loads(event["body"])
    else:
        payload = event

    # 2. Grab and decode the image_data
    image_bytes = base64.b64decode(payload["image_data"])

    # 3. Invoke the endpoint
    response = runtime.invoke_endpoint(
        EndpointName=ENDPOINT,
        ContentType="image/png",
        Body=image_bytes
    )
    result = response["Body"].read().decode("utf-8")

    # 4. Attach inferences back onto the same payload dict
    payload["inferences"] = result

    # 5. Return in the same shape Step Functions expect
    return {
        "statusCode": 200,
        "body": json.dumps(payload)
    }
