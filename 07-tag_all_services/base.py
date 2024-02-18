import boto3

# Cria uma sessão boto3
session = boto3.Session(profile_name='default')

# Cria um client para o serviço AWS Resource Groups Tagging API.
client = session.client('resourcegroupstaggingapi')

# Define a tag que será adicionada nos recursos
tag_key = "map-migrated"
tag_value = "mig0000"

try:
    # Varre todos os serviços disponíveis na conta
    for service_name in session.get_available_services():
        # Cria um client para o serviço atual
        client_service = session.client(service_name)

        # Verifica se o serviço atual suporta a operação "list_resources"
        if hasattr(client_service, 'list_resources') and callable(getattr(client_service, 'list_resources')):
            # Varre todos os recursos do serviço atual
            for resource in client_service.list_resources().get(service_name, []):
                # Obter a lista de tags do recurso
                tags = client.list_tags_for_resource(ResourceARN=resource).get('Tags', [])
                
                # Verificar se a tag "map-migrated" está presente na lista de tags
                if any(tag['Key'] == tag_key for tag in tags):
                    # Desconsiderar o recurso
                    print(f'O Recurso: {resource}, no serviço {service_name}, será desconsiderado.')
                else:
                    # Adicionar a tag "map-migrated" ao recurso usando o cliente 'resourcegroupstaggingapi'
                    client.tag_resource(ResourceARN=resource, Tags={tag_key: tag_value})
                    print(f"Recurso: {resource} no serviço {service_name} foi tagueado com a tag {tag_key}:{tag_value}")
        else:
            # Imprime uma mensagem se o cliente não suportar a operação list_resources.
            print(f'O serviço {service_name} não suporta a operação list_resources. Ignorando este serviço.')

except Exception as e:
    # Captura e imprime qualquer exceção ocorrida durante a execução, incluindo informações sobre o serviço e recurso
    print(f"Ocorreu um erro durante a execução. Detalhes: {e}")
