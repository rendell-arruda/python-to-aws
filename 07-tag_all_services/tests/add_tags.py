import boto3

session = boto3.Session(profile_name='default')

client = session.client('resourcegroupstaggingapi')
# arn fora do padrao nao funciona
arn_teste = 'arn:aws:payments::266549158321:payment-instrument:6ce10c47-424a-4c45-94ab-4afb71ab9d7a'

response = client.tag_resources(
    ResourceARNList=[
        arn_teste,
    ],
    Tags={
        'map': 'migrated'
    }
)