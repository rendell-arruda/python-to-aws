import json
import boto3
import csv
import os


def lambda_handler(event, context):
    # listar IDs das contas alvo
    accounts = ["266549158321", "471112936182"]
    role_name = "desbribe_ec2_details-role-jtvubyqy"

    for account_id in accounts:
        assumed_role = assume_role(account_id, role_name)
        if assumed_role:
            execute_task(assumed_role, account_id)


def assume_role(account_id, role_name):
    sts_client = boto3.client("sts")
    try:
        response = sts_client.assume_role(
            RoleArn=f"arn:aws:iam::{account_id}:role/{role_name}",
            RoleSessionName="LambdaSession",
        )
        credentials = response["Credentials"]
        return boto3.Session(
            aws_access_key_id=credentials["AccessKeyId"],
            aws_secret_access_key=credentials["SecretAccessKey"],
            aws_session_token=credentials["SessionToken"],
        )
    except Exception as e:
        print(f"Error assuming role for account {account_id}: {str(e)}")
        return None


def execute_task(session, account_id):

    # Crie um cliente EC2
    ec2_client = session.client("ec2")

    # Descreva instâncias EC2
    response = ec2_client.describe_instances()

    # Lista para armazenar detalhes das instâncias
    instances_details = []

    # Iterar sobre todas as respostas [Reservations]
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:

            # Pegar os detalhes da instância
            instance_id = instance["InstanceId"]
            # Pegar o estado da instância
            instance_state = instance["State"]["Name"]
            # pegar o type da instância
            instance_type = instance["InstanceType"]

            # ITERAR SOBRE TODAS AS TAGS DA INSTANCIA UMA VEZ
            # tag name
            name = None
            # tag schedule
            schedule = None
            # lista todas as tags da instância
            for tag in instance.get("Tags", []):
                if tag["Key"] == "Name":
                    name = tag["Value"]
                elif tag["Key"] == "Schedule":
                    schedule = tag["Value"]

            # pegar os ebs volumes da instancia
            ebs_volumes = []
            for volume in instance.get("BlockDeviceMappings", []):
                ebs_volumes.append(volume["Ebs"]["VolumeId"])

                # Converte a lista de IDs de volumes EBS em uma string concatenada
            ebs_volumes_str = ", ".join(ebs_volumes)

            # Adiciona os detalhes da instancia  na lista
            instances_details.append(
                {
                    "Account Id": account_id,  # Adiciona o ID da conta
                    "Instance Id": instance_id,
                    "Name": name,
                    "Instance State": instance_state,
                    "Instance Type": instance_type,
                    "Schedule": schedule,
                    "Ebs Volumes": ebs_volumes_str,
                }
            )

    # SALVAR OS DADOS EM FORMATO CSV.
    ##especificar o nome do arquivo de saida em csv
    csv_file = "/tmp/ec2_instances.csv"
    # ESPECIFICA AS COLUNAS
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
        with open(csv_file, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in instances_details:
                writer.writerow(data)
    except IOError:
        print("Erro de E/S")

    # print(f"Detalhes das instâncias EC2 foram salvos nos arquivos {json_file} e {csv_file}")

    ## enviar os dados para o S3
    # Enviar o arquivo CSV para um bucket S3
    s3_client = boto3.client("s3")
    bucket_name = "ilustredev-lambda-ec2-details-bucket"
    s3_key = "details/ec2_instances.csv"

    try:
        s3_client.upload_file(csv_file, bucket_name, s3_key)
        print(
            f"Arquivo {csv_file} foi enviado para o bucket S3 {bucket_name} com a chave {s3_key}."
        )
    except Exception as e:
        print(f"Erro ao enviar o arquivo para o bucket S3: {e}")

    return {"statusCode": 200, "body": json.dumps("Hello from Lambda!")}
