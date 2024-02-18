import boto3
# importa o modulo para regex
import re

# Cria uma expressão regular para validar ARNs
arn_pattern = re.compile(r'arn:aws:[a-z0-9\-]+:[a-z0-9\-]+:[0-9]+:[a-zA-Z0-9\-\/]+')

# Cria uma sessão do Boto3 usando um perfil chamado 'default'. No caso de uso de aws sso será importante usar
session = boto3.Session(profile_name='default')

# Cria um client para o serviço AWS Resource Groups Tagging API. 
# Esse cliente será usado para fazer chamadas à API da AWS.
client = session.client('resourcegroupstaggingapi')

# definir quais tags serao adicionadas 
tag_key = 'map-migrated'
tag_value = 'agoraVai'

try:
    # Faz uma chamada à operação get_resources para obter informações sobre os recursos.
    # O resultado é uma lista de dicionários, onde cada dicionário representa um recurso com suas tags.
    get_resources = client.get_resources()['ResourceTagMappingList']
    
    # Itera sobre todos os recursos retornados pela chamada get_resources.
    for resource in get_resources:
        # obtem o arn do recurso 
        resource_arn = resource['ResourceARN']
        print(resource_arn)
        
        #validar o arn com metodo match
        if arn_pattern.match(resource_arn): 
            # Obtém as tags do recurso. Se o recurso não tiver tags, retorna uma lista vazia.
            tags = resource.get('Tags',[])                
            
            # Verifica se a tag 'map-migrated' já existe no recurso.
            if any(tag['Key'] == tag_key for tag in tags):
                print(f'O resource: {resource_arn} já possui a tag {tag_key}')
                response = client.tag_resources(
                    ResourceARNList=[resource_arn],Tags={tag_key: tag_value})
                
            else:
                # Se a tag não existir, imprime uma mensagem indicando que o recurso será taggeado.
                print(f'O resource; {resource_arn} será tagueado')
                
                # Chama a operação tag_resources para adicionar a tag ao recurso.
                response = client.tag_resources(
                    ResourceARNList=[resource_arn],Tags={tag_key: tag_value})
            

# Captura exceções e imprime detalhes em caso de erro.
except Exception as e:
    print(e)