import logging
from botocore.exceptions import ClientError
import json
import boto3
import time

class LambdaWrapper:
    def __init__(self, lambda_client, iam_client, function_name=""):
        self.lambda_client = lambda_client
        self.iam_client = iam_client
        self.function_name = function_name
    
    def create_role(self, role_name):
        role_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": [
                            "lambda.amazonaws.com"
                        ]
                    },
                    "Action": [
                        "sts:AssumeRole"
                    ],
                }
            ]
        }
        response = self.iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(role_policy),
        )
        response = self.iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
        )

    def delete_role(self, role_name):
        # detach role policies
        role = boto3.resource('iam').Role(role_name)
        role.detach_policy(
            PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
        ) 
        # delete role
        self.iam_client.delete_role(RoleName=role_name)

    def create_function(self, handler_name, role_name, zipped_code):
        """
        Deploys a Lambda function.

        :param function_name: The name of the Lambda function.
        :param handler_name: The fully qualified name of the handler function. This
                             must include the file name and the function name.
        :param iam_role: The IAM role to use for the function.
        :param deployment_package: The deployment package that contains the function
                                   code in .zip format.
        :return: The Amazon Resource Name (ARN) of the newly created function.
        """
        try:
            # create the role for lambda function
            self.create_role(role_name)
            iam_role = self.iam_client.get_role(RoleName=role_name)  
            #time.sleep(10)
            response = self.lambda_client.create_function(
                FunctionName=self.function_name,
                Runtime='python3.9',
                Role=iam_role['Role']['Arn'],
                Handler=handler_name,
                Code={'ZipFile':zipped_code},
                Publish=True)
            function_arn = response['FunctionArn']
            waiter = self.lambda_client.get_waiter('function_active_v2')
            waiter.wait(FunctionName=self.function_name)
            # logger.info("Created function '%s' with ARN: '%s'.",
            #            function_name, response['FunctionArn'])
        except ClientError:
            logging.error("Couldn't create function %s.", self.function_name)
            raise
        else:
            return function_arn
    
    def delete_function(self, function_name, role_name):
        """
        Deletes a Lambda function.

        :param function_name: The name of the function to delete.
        """
        try:
            # self.lambda_client.delete_function(FunctionName=function_name)
            # delete role
            self.delete_role(role_name)
            
        except ClientError:
            logging.error("Couldn't delete function %s.", self.function_name)
            raise

    def add_permission(self, topic_arn):
        response = self.lambda_client.add_permission(
            FunctionName = self.function_name,
            StatementId='SNSInvokeSNS_triggered_Lambda',
            Action='lambda:InvokeFunction',
            Principal='sns.amazonaws.com',
            SourceArn= topic_arn
        )
     
    def delete_all_functions(self):
        """
        Lists the Lambda functions for the current account.
        """
        try:
            func_paginator = self.lambda_client.get_paginator('list_functions')
            for func_page in func_paginator.paginate():
                for func in func_page['Functions']:
                    self.delete_function(func['FunctionName'])
        except ClientError as err:
            logging.error(
                "Couldn't list functions. Here's why: %s: %s",
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
