import boto3

session = boto3.Session(profile_name='default')

client = session.client('resourcegroupstaggingapi')

# definir um metodo
tag_key = 'map-migrated'
tag_value = 'mig4777'
get_arn_resource = client.get_resources()['ResourceTagMappingList'][0]['ResourceARN']

resource_arn = get_arn_resource

response = client.tag_resources(
    ResourceARNList=[
        resource_arn,
    ],
    Tags={
        tag_key: tag_value
    }
)