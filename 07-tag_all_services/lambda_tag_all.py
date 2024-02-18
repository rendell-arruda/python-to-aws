import boto3

def lambda_handler(event, context):
    # Cria uma sessão boto3
    session = boto3.Session()

    # Cria um client para o serviço AWS Resource Groups Tagging API.
    client = session.client('resourcegroupstaggingapi')

    # Define a tag que será adicionada nos recursos
    tag_key = 'map-migrated'
    tag_value = 'mig34000'

    try:
        # Faz uma chamada à operação get_resources para obter informações sobre os recursos.
        # O resultado é uma lista de dicionários, onde cada dicionário representa um recurso com suas tags.
        get_resources = client.get_resources()['ResourceTagMappingList']

        # Itera sobre todos os recursos retornados pela chamada get_resources.
        for resource in get_resources:
            # Obtem o ARN do recurso 
            resource_arn = resource['ResourceARN']

            # Obtém as tags do recurso. Se o recurso não tiver tags, retorna uma lista vazia.
            tags = resource.get('Tags', [])                

            # Verifica se a tag 'map-migrated' já existe no recurso.
            if any(tag['Key'] == tag_key for tag in tags):
                continue
            else:
                # Se a tag não existir, imprime uma mensagem indicando que o recurso será taggeado.
                print(f'O recurso {resource_arn} será tagueado')

                # Chama a operação tag_resources para adicionar a tag ao recurso.
                response = client.tag_resources(
                    ResourceARNList=[resource_arn], Tags={tag_key: tag_value})

    # Captura exceções e imprime detalhes em caso de erro.
    except Exception as e:
        print(e)

# Este bloco permite executar o código localmente, facilitando testes.
if __name__ == "__main__":
    lambda_handler({}, {})
