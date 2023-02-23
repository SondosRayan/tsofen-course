import Topic
import  Lambda
import boto3

#------------DELETE--------------------
# delete_lambda
iam_client = boto3.client('iam')
lambda_client = boto3.client('lambda')
lambdaWrapper = Lambda.LambdaWrapper(lambda_client, iam_client)
function_name = 'SNS_triggered_Lambda'
role_name = 'lambda-sns-role'
lambdaWrapper.delete_function(function_name, role_name)

# delete topics and subscriptions
sns_client = boto3.client("sns", "us-east-1")
topicWrapper = Topic.TopicWrapper(sns_client)
topicWrapper.delete_all_topics()
topicWrapper.delete_all_subscriptions()

# delete log
logs_client = boto3.client('logs')
response = logs_client.delete_log_group(
    logGroupName='/aws/lambda/SNS_triggered_Lambda'
)
