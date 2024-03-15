import json
import boto3
from datetime import datetime, timezone, timedelta

dynamodb = boto3.client("dynamodb")
ec2 = boto3.client("ec2")


def lambda_handler(event, context):
    regions = ["us-east-1", "sa-east-1"]
    days_created = 0

    for region in regions:
        print(f"##### {region} #####")

        ec2 = boto3.client("ec2", region_name=region)
        paginator = ec2.get_paginator("describe_snapshots")
        snapshot_iterator = paginator.paginate(OwnerIds=["self"])

        for page in snapshot_iterator:
            snapshots = page["Snapshots"]

            for snapshot in snapshots:
                snapshot_id = snapshot["SnapshotId"]
                start_time = snapshot["StartTime"].replace(tzinfo=timezone.utc)
                difference = datetime.now(timezone.utc) - start_time

                if difference.days >= days_created:
                    dynamodb.put_item(
                        TableName="list_snapshots",
                        Item={
                            "SnapshotId": {"S": snapshot_id},
                        },
                    )

    return {
        "statusCode": 200,
        "body": json.dumps("Snapshots verificados e enviados para o DynamoDB"),
    }
