import boto3


session = boto3.Session(profile_name='default')
# cria um client(objeto) AWS Resource Groups Tagging API.
client = session.client('resourcegroupstaggingapi')

# retornar todos os atributos dos recursos da conta
get_resources = client.get_resources()['ResourceTagMappingList']

# lista as tags
tags = get_resources[0]['Tags']

# print(tags)

# Itera sobre todos os recursos retornados pela chamada get_resources.
for resource in get_resources:
    # Obtem o ARN do recurso             
    resource_arn = resource['ResourceARN']
    print(resource_arn)
