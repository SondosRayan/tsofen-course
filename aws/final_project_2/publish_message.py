import boto3


# Get the service resource
sns_client = boto3.client('sns')
topic_arn = "arn:aws:sns:us-east-1:993234544068:" + "my-topic"
for i in range(5):
    response = sns_client.publish(
        TopicArn = topic_arn,
        Message = '*** Finally :) ***',
        Subject = 'Important'
    )