import boto3
# importa o modulo para usar regex
import re

def lambda_handler(event, context):
    
    # Cria uma expressão regular para validar ARNs
    arn_pattern = re.compile(r'arn:aws:[a-z0-9\-]+:[a-z0-9\-]+:[0-9]+:[a-zA-Z0-9\-\/]+')

    # Cria uma sessão do Boto3 usando um perfil chamado 'default'. No caso de uso de aws sso será importante usar
    session = boto3.Session(profile_name='default')
    regions = session.get_available_regions('resourcegroupstaggingapi')
    
    # percorrer todas as regioes da contas
    for region in regions:
        print(f'entrando na regiao {region}')
        try:
            # Cria um client para chamadas ao serviço AWS Resource Groups Tagging API. 
            client = session.client('resourcegroupstaggingapi', region_name=region)

            # defini quais tags serao adicionadas 
            tag_key = 'map-mig'
            tag_value = 'to_cansado_ja'

            #armazenar os arns fora do padrao: APAGAR
            invalid_arns = []

            try:
                # Faz uma chamada à operação get_resources para obter uma lista de Dic com as infos dos recursos.
                get_resources = client.get_resources()['ResourceTagMappingList']
                
                # Itera sobre todos os recursos retornados pela chamada get_resources.
                for resource in get_resources:
                    # obtem o arn do recurso 
                    resource_arn = resource['ResourceARN']

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
                    # caso o arn fora di padrao
                    else:
                        print(f'O ARN: {resource_arn} não esta no padrão valido')
                        invalid_arns.append(resource_arn)
                        
                print("ARNS fora do padrão:", invalid_arns)    

            # Captura exceções e imprime detalhes em caso de erro.
            except Exception as e:
                print(e)
        except Exception as e:
            print(f'Exceções da região {region}', e)
#para teste no vs code 
if __name__ == '__main__':
    lambda_handler({},{})