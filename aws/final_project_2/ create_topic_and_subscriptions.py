import Topic
import Lambda
import boto3

#------------------------------------------------------------------------------
#  		TESTS
#------------------------------------------------------------------------------
def test_create(region_name = "us-east-1"):
    #------------TOPIC--------------------
    # Creates a topic
    sns_client = boto3.client('sns', region_name)
    topicWrapper = Topic.TopicWrapper(sns_client)
    topic_name = 'my-topic'
    topic = topicWrapper.create_topic(topic_name)
    # Creates an email subscription
    topic_arn = topic['TopicArn']
    endpoint = 'rayan1sondos@gmail.com'
    email_subscription = topicWrapper.add_subscription(topic_arn, 'email', endpoint)
    
    # Creates a phone subscription
    endpoint = '+972545613709'
    phone_subscription = topicWrapper.add_subscription(topic_arn, 'sms', endpoint)
    
    #------------LAMBDA--------------------
    # Creates a Lambda subscription
    iam_client = boto3.client('iam')
    lambda_client = boto3.client('lambda')
    function_name = 'SNS_triggered_Lambda'
    role_name = 'lambda-sns-role'
    lambdaWrapper = Lambda.LambdaWrapper(lambda_client, iam_client, function_name)
    with open('/home/osboxes/tsofen-course/aws/sns/lambda.zip', 'rb') as f:
        zipped_code = f.read()

    # role = iam_client.get_role(RoleName=role_name)    
    function_arn = lambdaWrapper.create_function(
                                  'handler.lambda_handler',
                                  role_name,
                                  zipped_code)
    lambdaWrapper.add_permission(topic_arn)
    # endpoint = 'arn:aws:lambda:us-east-1:993234544068:function:SNS_triggered_Lambda' # arn lmbda function
    lambda_subscription = topicWrapper.add_subscription(topic_arn, 'lambda', function_arn)
    

if __name__ == '__main__':
    topic_name = test_create()