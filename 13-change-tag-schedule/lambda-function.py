import boto3
import json

regions = ["us-east-1", "sa-east-1"]


def lambda_handler(event, context):

    for region in regions:
        session = boto3.Session(profile_name="default")
        client = session.client("ec2", region_name=region)

        try:
            response = client.describe_instances()
            for reservation in response["Reservations"]:
                for instance in reservation["Instances"]:
                    instance_Id = instance["InstanceId"]

                    for tag in instance.get("Tags", []):
                        if tag["Key"] == "Schedule":
                            schedule_value = tag["Value"]
                            # print(
                            #     f"Instance {instance_Id} has schedule {schedule_value}"
                            # )

        except Exception as e:
            print(f"Error describing instances: {str(e)}")
            return {
                "statusCode": 500,
                "body": json.dumps("Internal Server Error"),
            }


if __name__ == "__main__":
    lambda_handler({}, {})
