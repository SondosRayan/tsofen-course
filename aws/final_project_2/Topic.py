import logging
import boto3
from botocore.exceptions import ClientError


class TopicWrapper:
    def __init__(self, sns_client):
        self.sns_client = sns_client
        
    # Creates a SNS notification topic.
    def create_topic(self, name, region_name = "us-east-1"):
        try:
            topic = self.sns_client.create_topic(Name=name)
        except ClientError:
            logging.error(f'Could not create SNS topic {name}.')
            raise
        else:
            return topic
    
    # Subscribe to a topic using endpoint as email OR SMS OR Lambda
    def add_subscription(self, topic, protocol, endpoint, region_name = "us-east-1"):
        try:
            subscription = self.sns_client.subscribe(
                TopicArn=topic,
                Protocol=protocol,
                Endpoint=endpoint,
                ReturnSubscriptionArn=True)
        except ClientError:
            logging.error(
                "Couldn't subscribe {protocol} {endpoint} to topic {topic}.")
            raise
        else:
            return subscription
    
    def list_topics(self):
        """
        Lists topics for the current account.

        :return: An iterator that yields the topics.
        """
        sns_resource = boto3.resource('sns')
        topics_iter = sns_resource.topics.all()
        return topics_iter

    @staticmethod
    def delete_topic(topic):
        """
        Deletes a topic. All subscriptions to the topic are also deleted.
        """
        topic.delete()

    def delete_all_topics(self):
        for topic in self.list_topics():
            self.delete_topic(topic)

    def list_subscriptions(self):
        """
        Lists subscriptions for the current account.

        :return: An iterator that yields the subscriptions.
        """
        sns_resource = boto3.resource('sns')
        subscriptions_iter = sns_resource.subscriptions.all()
        return subscriptions_iter
    
    # Unsubscribes and deletes a subscription.
    def delete_subscription(self, subscription):
        try:
            subscription.delete()
        except ClientError:
            logging.error("Couldn't delete subscription %s.", subscription.arn)
            raise
    
    def delete_all_subscriptions(self):
        for subscription in self.list_subscriptions():
            self.delete_subscription(subscription)