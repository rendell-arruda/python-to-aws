import boto3

session = boto3.Session(profile_name='default')

client = session.client('resourcegroupstaggingapi')

# definir um metodo
tag_key = 'map-migrated'
tag_value = 'mig4777'
resource_arn = 'arn:aws:ec2:us-east-1:266549158321:instance/i-0354051ed688a8171'

response = client.tag_resources(
    ResourceARNList=[
        resource_arn,
    ],
    Tags={
        tag_key: tag_value
    }
)