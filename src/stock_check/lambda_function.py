"""
Lambda function that checks the product stock from a URL.
"""

import logging
import os

import boto3
import cytoolz.itertoolz as it
import requests

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Cache sns client at top level for lambda warm starts.
sns = boto3.client("sns")


def config(event):
    """Build the configuration from a passed in event and the environment."""
    return {
        "url": it.get("url", event, default=None),
        "timeout": it.get("timeout", event, default=15),
        "headers": it.get("headers", event, default=None),
        "match": it.get("match", event, default=None),
        "match_description": it.get("match_description", event, default="Your item"),
        "sns_topic_arn": os.getenv("SNS_TOPIC_ARN", default=None),
    }


def check_stock(cfg):
    """Check stock at a URL for a match."""
    logger.info("Checking stock at: %s", it.get("url", cfg))
    resp = requests.get(
        url=it.get("url", cfg),
        timeout=it.get("timeout", cfg),
        headers=it.get("headers", cfg),
    )

    logger.info("Response status code: %s", resp.status_code)

    logger.info("Checking for '%s' in response text.", it.get("match", cfg))
    if it.get("match", cfg) in resp.text:
        return "AVAILABLE"
    return "OUT OF STOCK"


def notify(cfg, item_status):
    """Send a notification if the item is available."""
    if item_status == "AVAILABLE":
        logger.info(
            "Publishing notification to topic: %s", it.get("sns_topic_arn", cfg, None)
        )
        sns.publish(
            TopicArn=it.get("sns_topic_arn", cfg, None),
            Subject=f"AWS SNS Notification: {it.get('match_description', cfg)} is AVAILABLE.",
            Message=f"{it.get('match_description', cfg)} is AVAILABLE.\nURL: {it.get('url', cfg)}",
        )


def lambda_handler(event, context):
    """Use the incoming `event` to check the response text from a `url` for a `match`."""
    logger.info("Incoming event: %s", event)

    cfg = config(event)
    logger.info("Using configuration: %s", cfg)

    item_status = check_stock(cfg)
    logger.info("%s is: %s.", it.get("match_description", cfg), item_status)

    notify(cfg, item_status)

    return {
        "body": "stock check results",
        "item_description": it.get("match_description", cfg),
        "item_status": item_status,
        "statusCode": 200,
    }
