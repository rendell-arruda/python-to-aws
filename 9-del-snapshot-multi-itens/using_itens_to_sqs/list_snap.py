import boto3
import os
import json
from datetime import datetime

# Inicializa o cliente do Boto3
ec2 = boto3.client("ec2")
sqs = boto3.client("sqs")
dynamodb = boto3.client("dynamodb")

# URL da fila SQS
SQS_QUEUE_URL = "<sua_url_da_fila_sqs>"

# Nome da tabela DynamoDB
DYNAMODB_TABLE_NAME = "<nome_da_tabela_dynamodb>"


def lambda_handler(event, context):
    # Obtém o token de páginação da última execução, se disponível
    last_evaluated_key = get_last_evaluated_key()

    # Cria um Paginator para listar os snapshots
    paginator = ec2.get_paginator("describe_snapshots")

    # Se houver um token de páginação da execução anterior, use-o
    if last_evaluated_key:
        page_iterator = paginator.paginate(StartingToken=last_evaluated_key)
    else:
        page_iterator = paginator.paginate()

    # Itera sobre os snapshots usando o paginator
    for page in page_iterator:
        for snapshot in page["Snapshots"]:
            process_snapshot(snapshot)

        # Salva o token de páginação (NextToken) no DynamoDB
        save_next_token(page["NextToken"])

    return {
        "statusCode": 200,
        "body": json.dumps("Processamento de snapshots concluído!"),
    }


def process_snapshot(snapshot):
    # Obtém a data de criação do snapshot
    creation_date = snapshot["StartTime"]

    # Calcula os dias desde a criação
    dias_desde_criacao = (datetime.now() - creation_date).days

    # Obtém o limite de idade do snapshot da variável de ambiente
    limite_idade_snapshot = int(os.environ.get("LIMITE_IDADE_SNAPSHOT", 7))

    # Se o snapshot for mais antigo que o limite, envie-o para a SQS
    if dias_desde_criacao > limite_idade_snapshot:
        # Envia o snapshot para a fila SQS
        sqs.send_message(QueueUrl=SQS_QUEUE_URL, MessageBody=json.dumps(snapshot))


def get_last_evaluated_key():
    # Recupera o LastEvaluatedKey do DynamoDB
    response = dynamodb.get_item(
        TableName=DYNAMODB_TABLE_NAME, Key={"Key": {"S": "LastEvaluatedKey"}}
    )

    if "Item" in response:
        return response["Item"]["Value"]["S"]
    else:
        return None


def save_next_token(next_token):
    # Salva o token de páginação (NextToken) no DynamoDB
    dynamodb.put_item(
        TableName=DYNAMODB_TABLE_NAME,
        Item={"Key": {"S": "LastEvaluatedKey"}, "Value": {"S": next_token}},
    )
