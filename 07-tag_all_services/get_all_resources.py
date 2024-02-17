import boto3


session = boto3.Session(profile_name='default')
# cria um client(objeto) AWS Resource Groups Tagging API.
client = session.client('resourcegroupstaggingapi')

# retornar todos os servicos da conta com seus atributos
# Esta operação retorna uma lista de recursos e seus atributos.
get_arn_resource = client.get_resources()['ResourceTagMappingList'][0]['ResourceARN']

# tags = client.get_resources()['ResourceTagMappingList'][0]['Tags']


print(get_arn_resource)