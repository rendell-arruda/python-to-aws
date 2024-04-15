import boto3

s3_client = boto3.client("s3")

lifecycle_configuration = {
    "Rules": [
        {
            "Expiration": {
                "Days": 30,
            },
            "ID": "ExpiratedRole",
            "Prefix": "",
            "Status": "Enabled",
        },
    ]
}


def put_bucket_lifecycle_configuration(bucket_name):

    response = s3_client.put_bucket_lifecycle_configuration(
        Bucket=bucket_name, LifecycleConfiguration=lifecycle_configuration
    )


def list_buckets():
    buckets = s3_client.list_buckets()
    for bucket in buckets["Buckets"]:
        bucket_name = bucket["Name"]
        # print(bucket_name)
        put_bucket_lifecycle_configuration(bucket_name)
        print(f"Politica aplicada com sucesso no bucket {bucket_name}")


list_buckets()
