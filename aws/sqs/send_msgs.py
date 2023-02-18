import boto3
import json


# Get the service resource
sqs = boto3.resource('sqs')

# Get the queue
queue = sqs.get_queue_by_name(QueueName='Qone')
queue_url = 'https://sqs.us-east-1.amazonaws.com/993234544068/Qone'

# send messsage to the queue
response = queue.send_message(QueueUrl=queue_url, MessageBody='Hi !!!, I am sending message')