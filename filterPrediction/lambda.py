import json

THRESHOLD = 0.93

def lambda_handler(event, context):
    # 1. Grab the inferences (could be a JSON string or a Python list)
    raw_infs = event["inferences"]
    if isinstance(raw_infs, str):
        inferences = json.loads(raw_infs)
    else:
        inferences = raw_infs

    # 2. Check if any value exceeds the threshold
    meets_threshold = any(pred > THRESHOLD for pred in inferences)

    # 3. Succeed or fail
    if not meets_threshold:
        # This will bubble up and cause the Step Function to enter its Fail state
        raise Exception("THRESHOLD_CONFIDENCE_NOT_MET")

    # 4. Return the original event so downstream steps can use it
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
