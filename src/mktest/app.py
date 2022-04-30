import json
import boto3

BUCKET_NAME = 'questions-and-answers-files'

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('qanda')


def lambda_handler(event, context):
    # test_title = os.path.splitext(os.path.basename(fname))[0]
    questions = []

    return {
        "statusCode": 200,
        "body": json.dumps({
            "questions": questions,
        }),
    }
