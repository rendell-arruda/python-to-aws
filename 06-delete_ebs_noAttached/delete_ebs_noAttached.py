import boto3
import csv

# Criar uma instancia do client EC2 na região us-east-1
ec2 = boto3.resource("ec2", region_name="us-east-1")

#funcao lambda principal
import boto3

import boto3

def lambda_handler(event, context):
    # Criar um recurso EC2
    ec2 = boto3.resource('ec2')

    # Inicializar listas
    ebs_excluidos = []
    ebs_nao_excluidos = []

    # Inicializar contador
    count_ebs_excluidos = 0

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

    # Imprimir listas e contador
    print("\nEBS Excluídos:")
    print("\n".join(ebs_excluidos))

    print("\nEBS Não Excluídos:")
    print("\n".join(ebs_nao_excluidos))

    print(f'\nNúmero total de EBS excluídos: {count_ebs_excluidos}')
    
    # enviar um email
    send_email(count_ebs_excluidos,ebs_nao_excluidos)

# Este bloco permite que o código seja testado localmente, mas não é executado na AWS Lambda.
if __name__ == '__main__':
    lambda_handler(None, None)



def send_email(count_ebs_excluidos,ebs_nao_excluidos):
    # ... (código existente)

    # Publicar mensagem no tópico SNS
    sns_topic_arn = "arn:aws:sns:us-east-1:266549158321:email_ebs_unattached"
    sns_client = boto3.client('sns')

    message = "A função Lambda foi executada com sucesso! Foram excluídos com sucesso"
    subject = "Exclusão de Volumes EBS untached na conta XPTO"

    sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=message,
        Subject=subject
    )

# Este bloco permite que o código seja testado localmente, mas não é executado na AWS Lambda.
if __name__ == '__main__':
    lambda_handler(None, None)
