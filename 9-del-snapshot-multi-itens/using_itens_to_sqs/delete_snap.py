import boto3
import json

# Inicializa o cliente do Boto3
ec2 = boto3.client("ec2")


def lambda_handler(event, context):
    # Itera sobre as mensagens recebidas da fila SQS
    for record in event["Records"]:
        message_body = json.loads(record["body"])
        snapshot_id = message_body["SnapshotId"]

        # Deleta o snapshot
        ec2.delete_snapshot(SnapshotId=snapshot_id)

    return {"statusCode": 200, "body": json.dumps("Snapshots deletados com sucesso!")}
