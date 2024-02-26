import boto3
import csv

regions = ['us-east-1', 'sa-east-1']

def send_email(count_ebs_excluidos_por_regiao, count_ebs_nao_excluidos_por_regiao, ebs_nao_excluidos):
    # ... (código existente)

    # Publicar mensagem no tópico SNS
    sns_topic_arn = "arn:aws:sns:us-east-1:266549158321:finops_ebs_unattached"
    sns_client = boto3.client('sns')

    # Formatando a mensagem para incluir o número de EBS excluídos e não excluídos em cada região
    message = "A função Lambda foi executada com sucesso!\n"
    for regiao, count_excluidos in count_ebs_excluidos_por_regiao:
        count_nao_excluidos = next((count for reg, count in count_ebs_nao_excluidos_por_regiao if reg == regiao), 0)
        message += f"{count_excluidos} foram excluídos e {count_nao_excluidos} não foram excluídos na região {regiao}\n"
    message += f"Total de EBS excluídos: {sum([count for _, count in count_ebs_excluidos_por_regiao])}.\n"
    message += f"Total de EBS não excluídos: {sum([count for _, count in count_ebs_nao_excluidos_por_regiao])}.\n"
    subject = "Exclusão de Volumes EBS unattached na conta: Observability-dev"

    sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=message,
        Subject=subject
    )

#funcao lambda principal

def lambda_handler(event, context):
    count_ebs_excluidos_por_regiao = [] # lista para armazenar o número de EBS excluídos em cada região
    count_ebs_nao_excluidos_por_regiao = [] # lista para armazenar o número de EBS não excluídos em cada região
    
    for region in regions:
        print(f'#### {region} ####')

        # Criar uma instancia do client EC2
        ec2 = boto3.resource("ec2",region_name=region)

        # Inicializar listas
        ebs_excluidos = []
        ebs_nao_excluidos = []

        # Inicializar contador
        count_ebs_excluidos = 0
        count_ebs_nao_excluidos = 0

        # Iterar sobre todos os volumes EBS na região
        for volume in ec2.volumes.all():
            # Verificar se o volume não está anexado a uma instância
            if not volume.attachments:
                # Criar um dicionário com as tags para facilitar a verificação
                tags = {tag['Key']: tag['Value'] for tag in volume.tags} if volume.tags else {}

                # Verificar se o volume possui a tag 'inUse' com valor True
                if 'inUse' in tags and tags['inUse'].lower() == 'true':
                    print(f'Volume {volume.id} não pode ser excluído pois está marcado como em uso')
                    ebs_nao_excluidos.append(volume.id)
                    count_ebs_nao_excluidos += 1
                else:
                    # Se o volume não possuiu a tag 'inUse', pode ser excluído
                    volume.delete()
                    print(f'Volume {volume.id} excluído com sucesso')
                    ebs_excluidos.append(volume.id)
                    count_ebs_excluidos += 1
            else:
                # Se o volume está anexado a uma instância
                print(f'O volume {volume.id} está anexado a uma instância')
                ebs_nao_excluidos.append(volume.id)
                count_ebs_nao_excluidos += 1

        # Imprimir listas e contador
        print("\nEBS Excluídos:")
        print("\n".join(ebs_excluidos))

        print("\nEBS Não Excluídos:")
        print("\n".join(ebs_nao_excluidos))

        print(f'\nNúmero total de EBS excluídos: {count_ebs_excluidos}')
        print(f'Número total de EBS não excluídos: {count_ebs_nao_excluidos}')

        # Adicionar o número de EBS excluídos e não excluídos na região à lista
        count_ebs_excluidos_por_regiao.append((region, count_ebs_excluidos))
        count_ebs_nao_excluidos_por_regiao.append((region, count_ebs_nao_excluidos))

    # enviar um email com o número de EBS excluídos e não excluídos em cada região
    send_email(count_ebs_excluidos_por_regiao, count_ebs_nao_excluidos_por_regiao, ebs_nao_excluidos)

