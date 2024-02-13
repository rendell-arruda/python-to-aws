import boto3

# Criar uma instancia do client EC2 na região us-east-1
ec2 = boto3.resource("ec2", region_name="us-east-1")

#funcao lambda principal
def lambda_handler(event, context):
    # Itera sobre todos os volumes EBS na região
    for volume in ec2.volumes.all():
        # verifica se o volume não esta anexado a uma instancia
        if not volume.attachments:
            # cria um dicionario com as tags para facilitar a verificacao
            tags = {tag['Key']: tag['Value'] for tag in volume.tags}

            # Verifica se o volume possui a tag 'InUse' com valor True
            if 'inUse' in tags and tags ['inUse'] =='true':
                print(f'Volume {volume.id} não pode ser excluídos pois esta marcado como emUso')
            
            else:
                volume.delete()
                print(f'Volume {volume.id} excluído com sucesso')
        else:
            # se o volume estiver anexado a uma instancia
            print(f'O volume {volume.id} está anexado a instancia')