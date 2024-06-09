import json  # Importa o módulo json para trabalhar com dados JSON.
import boto3  # Importa o módulo boto3 para interagir com os serviços da AWS.
import csv  # Importa o módulo csv para trabalhar com arquivos CSV.
import os  # Importa o módulo os para interagir com o sistema operacional.


def lambda_handler(event, context):
    # Lista de IDs das contas alvo.
    accounts = ["266549158321", "471112936182"]
    # Nome da role a ser assumida nas contas alvo.
    role_name = "desbribe_ec2_details-role-jtvubyqy"

    # Para cada ID de conta na lista de contas.
    for account_id in accounts:
        # Assume a role na conta especificada.
        assumed_role = assume_role(account_id, role_name)
        # Se a role foi assumida com sucesso, executa a tarefa.
        if assumed_role:
            execute_task(assumed_role, account_id)


def assume_role(account_id, role_name):
    # Cria um cliente STS para realizar a operação assume_role.
    sts_client = boto3.client("sts")
    try:
        # Tenta assumir a role especificada na conta alvo.
        response = sts_client.assume_role(
            RoleArn=f"arn:aws:iam::{account_id}:role/{role_name}",  # ARN da role a ser assumida.
            RoleSessionName="LambdaSession",  # Nome da sessão.
        )
        # Extrai as credenciais da resposta.
        credentials = response["Credentials"]
        # Retorna uma sessão boto3 com as credenciais temporárias.
        return boto3.Session(
            aws_access_key_id=credentials["AccessKeyId"],
            aws_secret_access_key=credentials["SecretAccessKey"],
            aws_session_token=credentials["SessionToken"],
        )
    except Exception as e:
        # Em caso de erro, imprime uma mensagem de erro.
        print(f"Error assuming role for account {account_id}: {str(e)}")
        return None


def execute_task(session, account_id):
    # Cria um cliente EC2 usando a sessão assumida.
    ec2_client = session.client("ec2")

    # Descreve instâncias EC2 na conta alvo.
    response = ec2_client.describe_instances()

    # Lista para armazenar os detalhes das instâncias.
    instances_details = []

    # Itera sobre todas as reservas de instâncias.
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            # Pega os detalhes da instância.
            instance_id = instance["InstanceId"]
            instance_state = instance["State"]["Name"]
            instance_type = instance["InstanceType"]

            # Inicializa as tags name e schedule como None.
            name = None
            schedule = None
            # Itera sobre as tags da instância.
            for tag in instance.get("Tags", []):
                if tag["Key"] == "Name":
                    name = tag["Value"]
                elif tag["Key"] == "Schedule":
                    schedule = tag["Value"]

            # Lista para armazenar os IDs dos volumes EBS.
            ebs_volumes = []
            for volume in instance.get("BlockDeviceMappings", []):
                ebs_volumes.append(volume["Ebs"]["VolumeId"])

            # Converte a lista de IDs de volumes EBS em uma string.
            ebs_volumes_str = ", ".join(ebs_volumes)

            # Adiciona os detalhes da instância na lista.
            instances_details.append(
                {
                    "Account Id": account_id,  # Adiciona o ID da conta.
                    "Instance Id": instance_id,
                    "Name": name,
                    "Instance State": instance_state,
                    "Instance Type": instance_type,
                    "Schedule": schedule,
                    "Ebs Volumes": ebs_volumes_str,
                }
            )

    # Especifica o nome do arquivo de saída CSV.
    csv_file = "/tmp/ec2_instances.csv"
    # Especifica as colunas do CSV.
    csv_columns = [
        "Account Id",
        "Instance Id",
        "Name",
        "Instance State",
        "Instance Type",
        "Schedule",
        "Ebs Volumes",
    ]

    try:
        # Abre o arquivo CSV para escrita.
        with open(csv_file, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()  # Escreve o cabeçalho.
            for data in instances_details:
                writer.writerow(data)  # Escreve os dados das instâncias.
    except IOError:
        # Em caso de erro de I/O, imprime uma mensagem.
        print("Erro de E/S")

    # Cria um cliente S3.
    s3_client = boto3.client("s3")
    # Nome do bucket e chave do objeto no S3.
    bucket_name = "ilustredev-lambda-ec2-details-bucket"
    s3_key = "details/ec2_instances.csv"

    try:
        # Faz upload do arquivo CSV para o bucket S3.
        s3_client.upload_file(csv_file, bucket_name, s3_key)
        print(
            f"Arquivo {csv_file} foi enviado para o bucket S3 {bucket_name} com a chave {s3_key}."
        )
    except Exception as e:
        # Em caso de erro no upload, imprime uma mensagem.
        print(f"Erro ao enviar o arquivo para o bucket S3: {e}")

    # Retorna uma resposta de sucesso.
    return {"statusCode": 200, "body": json.dumps("Hello from Lambda!")}
