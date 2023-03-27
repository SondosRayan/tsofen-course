import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    
    client = boto3.client('sqs')
    message_body = json.dumps(event)
    queue_url = 'https://sqs.us-east-1.amazonaws.com/993234544068/s3_queue'
    
    response = client.send_message(
        QueueUrl=queue_url,
        MessageBody=message_body
    )
    
    print(response)
    print("This is massege from lambda1 -Hadeel-")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }