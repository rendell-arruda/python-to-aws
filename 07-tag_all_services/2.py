import boto3
# Cria uma sessão botos
session = boto3.Session(profile_name='observability-dev')

client = session.client('resourcegroupstaggingapi')
# Define a tag que será adicionada nos recursos
tag_key = "map-migrated"
tag_value = "mig23769"

service_list = session.get_avalable_services()

# em todos os recursos # Varre todos os serviços disponíveis na conta 
for service in service_list:
    # Cria um client para o serviço atual
    client = session.client (service)
    # Verifica se o serviço atual suporta a operação "list_tags_for resource" 
    if 'list_tags_for_resource' in dir(client):
        # Varre todos os recursos do serviço atual 
        for resource in client.list_resources().get(service, []):
        # Obter a lista de tags do recurso
            tags=client.list_tags_for_resource(ResourceArn=resource).get ('Tags', [])
        # Verificar se a tag "map-migrated" está presente na lista de tags
    
        if any(tag['Key'] == tag_key for tag in tags):
        # Desconsiderar o recurso
          print (f'O Recurso: {resource}, será desconsiderado.')
        else:
        # Adicionar a tag "map-migrated" ao recurso
            client.tag_resource(ResourceArn=resource, Tags={tag_key: tag_value,})
            print(f"Recurso: {resource} foi tagueado com a tag")