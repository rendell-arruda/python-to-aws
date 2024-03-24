import boto3
import os
import json
import time
from datetime import datetime, timedelta

# Define o número de dias para comparar com as snapshots
DAYS_THRESHOLD = 7

# Define o nome da fila SQS para enviar as snapshots antigas
SQS_QUEUE_NAME = "old-snapshots"

# Define o nome da tabela DynamoDB para armazenar informações de paginação
DYNAMODB_TABLE_NAME = "snapshot-pagination"

# Inicializa os clientes da AWS
ec2 = boto3.client("ec2")
sqs = boto3.client("sqs")
dynamodb = boto3.resource("dynamodb")


def lambda_handler(event, context):
    # Obtém o token de paginação da última chamada, se houver
    last_pagination_token = get_last_pagination_token()

    # Cria um paginador para listar todas as snapshots na organização
    paginator = ec2.get_paginator("describe_snapshots")
    page_iterator = paginator.paginate(
        OwnerIds=["self"],
        PaginationConfig={"PageSize": 1000, "StartingToken": last_pagination_token},
    )

    # Percorre todas as snapshots
    for page in page_iterator:
        # Armazena o token de paginação da página atual
        store_last_pagination_token(page["NextToken"])
        for snapshot in page["Snapshots"]:
            # Verifica se a snapshot é mais antiga do que o limite
            snapshot_age = datetime.now() - snapshot["StartTime"].replace(tzinfo=None)
            if snapshot_age.days >= DAYS_THRESHOLD:
                # Envia o ID da snapshot para a fila SQS
                sqs.send_message(
                    QueueUrl=get_queue_url(),
                    MessageBody=json.dumps({"snapshot_id": snapshot["SnapshotId"]}),
                )


def get_last_pagination_token():
    # Obtém o token de paginação da última chamada do DynamoDB
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    response = table.get_item(Key={"id": "last_pagination_token"})
    if "Item" in response:
        return response["Item"]["pagination_token"]
    else:
        return None


def store_last_pagination_token(pagination_token):
    # Armazena o token de paginação da última chamada no DynamoDB
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    table.put_item(
        Item={"id": "last_pagination_token", "pagination_token": pagination_token}
    )


def get_queue_url():
    # Obtém a URL da fila SQS
    response = sqs.get_queue_url(QueueName=SQS_QUEUE_NAME)
    return response["QueueUrl"]


# Este código deve ser implantado como uma função Lambda e configurado para ser executado em um cronograma.
# Ele listará todas as snapshots na organização, comparará com a variável DAYS_THRESHOLD e enviará os IDs das snapshots
# antigas para uma fila SQS chamada old-snapshots. Ele também armazenará o ID da última snapshot processada em uma tabela DynamoDB
# chamada snapshot-pagination, para que possa continuar de onde parou se o processo não foi concluído na última execução.
# Você precisará criar uma segunda função Lambda para consumir a fila old-snapshots e excluir as snapshots antigas.
