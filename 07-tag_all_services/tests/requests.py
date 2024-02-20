import boto3

def obter_recursos():
    # Inicializa a sessão e o cliente para o resourcegroupstaggingapi
    session = boto3.Session(profile_name='default')
    regions = session.get_available_regions('resourcegroupstaggingapi')
    # Faz uma chamada à operação get_resources para obter uma lista de Dic com as infos dos recursos.

    # Itera sobre cada regiao
    for region in regions:
        try:
            print(f'entrando na regiao {region}')
            # cria um client na regiao especifica
            client = session.client('resourcegroupstaggingapi',region_name=region)
            # faz um get nos recursos da regiao
            recursos = client.get_resources()['ResourceTagMappingList']
            # intera entre os recursos e lista
            for recurso in recursos:
                # Imprime informações sobre cada recurso
                print(f'{recurso}\n')
        except Exception as e:
            print(e)
        
if __name__ == "__main__":
    obter_recursos()
