import boto3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configurações para o envio de e-mail
smtp_server = 'your-smtp-server'
smtp_port = 587
smtp_username = 'your-smtp-username'
smtp_password = 'your-smtp-password'
sender_email = 'sender@example.com'
recipient_email = 'recipient@example.com'

def send_email(subject, body):
    # Configuração da mensagem
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Configuração da conexão SMTP
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, recipient_email, message.as_string())

def lambda_handler(event, context):
    try:
        # Criar contadores para volumes excluídos e volumes com erro
        volumes_excluidos = 0
        volumes_com_erro = 0

        # Obtém uma lista de todas as regiões disponíveis na conta
        regions = [region['RegionName'] for region in boto3.client('ec2').describe_regions()['Regions']]

        # Itera sobre todas as regiões
        for region in regions:
            # Criar uma instância do client EC2 na região atual
            ec2 = boto3.resource("ec2", region_name=region)

            # Iterar sobre todos os volumes EBS na região
            for volume in ec2.volumes.all():
                # Verifica se o volume não está anexado a uma instância
                if not volume.attachments:
                    # Criar um dicionário com as informações do volume para facilitar a verificação
                    volume_info = {
                        'ID': volume.id,
                        'Size': volume.size,
                        'State': volume.state,
                        'Tags': volume.tags
                    }

                    # Verifica se o volume possui a tag 'inUse' com valor True
                    if 'inUse' in volume_info['Tags'] and volume_info['Tags']['inUse'] == 'true':
                        print(f'Volume {volume.id} não pode ser excluído pois está marcado como emUso')
                        volumes_com_erro += 1
                    else:
                        volume.delete()
                        print(f'Volume {volume.id} excluído com sucesso em {region}')
                        volumes_excluidos += 1
                else:
                    # Se o volume estiver anexado a uma instância
                    print(f'O volume {volume.id} está anexado a instância em {region}')

        # Enviar e-mail com informações sobre volumes excluídos e volumes com erro
        send_email('Resumo da Exclusão de Volumes EBS', f'Volumes excluídos com sucesso: {volumes_excluidos}\nVolumes com erro: {volumes_com_erro}')

    except Exception as e:
        print(f'Ocorreu um erro: {e}')
        send_email('Erro durante a execução da Lambda', f'Ocorreu um erro durante a execução da Lambda: {e}')
