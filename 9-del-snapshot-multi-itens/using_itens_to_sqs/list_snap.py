import boto3
import json
import botocore.exceptions
import datetime

sqs_queue_url = "https://sqs.us-east-1.amazonaws.com/266549158321/fila_snap_sqs"
dynamodb_table_name = "snapshot-pagination"
dynamodb_partition_key = "pagination"
ec2_regions = ["us-east-1"]
days_created = 0

sqs = boto3.client("sqs")
dynamodb = boto3.client("dynamodb")


def lambda_handler(event, context):
    # Lê o próximo token de paginação da tabela do DynamoDB
    response = dynamodb.get_item(
        TableName=dynamodb_table_name, Key={"pagination": {"S": dynamodb_partition_key}}
    )
    next_token_item = response.get("Item", {}).get("next_token")
    next_token = next_token_item.get("S") if next_token_item else None

    for region in ec2_regions:
        print(f"##### {region} #####")

        ec2 = boto3.client("ec2", region_name=region)

        # Define o número máximo de resultados por chamada da API
        max_results = 1000

        # Define o token de paginação inicial
        starting_token = next_token

        # Itera sobre as páginas de snapshots
        while True:
            try:
                if starting_token is not None:
                    response = ec2.describe_snapshots(
                        OwnerIds=["self"],
                        MaxResults=max_results,
                        NextToken=starting_token,
                    )
                else:
                    response = ec2.describe_snapshots(
                        OwnerIds=["self"], MaxResults=max_results
                    )

                snapshots = response["Snapshots"]

                # Debugging: Verifica se os snapshots estão sendo encontrados
                print(f"Found {len(snapshots)} snapshots.")

                # Envia os IDs dos snapshots para a fila SQS
                for snapshot in snapshots:
                    snapshot_id = snapshot["SnapshotId"]
                    # Verifica se o snapshot foi criado há mais de 7 dias
                    snapshot_date = snapshot["StartTime"].date()
                    if (datetime.date.today() - snapshot_date).days >= days_created:
                        message_body = {"snapshot_id": snapshot_id, "region": region}
                        sqs.send_message(
                            QueueUrl=sqs_queue_url, MessageBody=json.dumps(message_body)
                        )
                        # Debugging: Imprime o ID do snapshot enviado
                        print(f"Sent snapshot ID {snapshot_id} to SQS.")
                    else:
                        # Debugging: Imprime o ID do snapshot e indica que não está sendo enviado para a fila
                        print(
                            f"Snapshot ID {snapshot_id} not sent to SQS because it's not older than 7 days."
                        )

                # Atualiza o token de paginação para a próxima página, se existir
                next_token = response.get("NextToken")
                if not next_token:
                    break

                # Armazena o valor do "NextToken" na tabela do DynamoDB
                dynamodb.put_item(
                    TableName=dynamodb_table_name,
                    Item={
                        "pagination": {"S": dynamodb_partition_key},
                        "next_token": {"S": next_token},
                    },
                )

                # Define o token de paginação inicial para a próxima página
                starting_token = next_token

            except botocore.exceptions.ClientError as e:
                if (
                    e.response["Error"]["Code"] == "InvalidParameterValue"
                    and "The token has expired" in e.response["Error"]["Message"]
                ):
                    # O token de paginação expirou, obtenha um novo token de paginação e continue a recuperar os snapshots
                    response = ec2.describe_snapshots(
                        OwnerIds=["self"], MaxResults=max_results
                    )
                    snapshots = response["Snapshots"]
                    for snapshot in snapshots:
                        snapshot_id = snapshot["SnapshotId"]
                        # Verifica se o snapshot foi criado há mais de 7 dias
                        snapshot_date = snapshot["StartTime"].date()
                        if (datetime.date.today() - snapshot_date).days > days_created:
                            message_body = {
                                "snapshot_id": snapshot_id,
                                "region": region,
                            }
                            sqs.send_message(
                                QueueUrl=sqs_queue_url,
                                MessageBody=json.dumps(message_body),
                            )
                            # Debugging: Imprime o ID do snapshot enviado
                            print(f"Sent snapshot ID {snapshot_id} to SQS.")
                        else:
                            # Debugging: Imprime o ID do snapshot e indica que não está sendo enviado para a fila
                            print(
                                f"Snapshot ID {snapshot_id} not sent to SQS because it's not older than 7 days."
                            )
                    next_token = response.get("NextToken")
                    if not next_token:
                        break
                    dynamodb.put_item(
                        TableName=dynamodb_table_name,
                        Item={
                            "pagination": {"S": dynamodb_partition_key},
                            "next_token": {"S": next_token},
                        },
                    )
                    starting_token = next_token
                else:
                    raise e

    return {
        "statusCode": 200,
        "body": json.dumps(
            "IDs dos snapshots enviados para a fila SQS e próximo token de paginação atualizado no DynamoDB"
        ),
    }
