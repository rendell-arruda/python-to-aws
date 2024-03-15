import json
import boto3

ec2 = boto3.client("ec2")
dynamodb = boto3.client("dynamodb")
sqs = boto3.client("sqs")


def lambda_handler(event, context):
    # Recuperar IDs dos snapshots armazenados no DynamoDB
    response = dynamodb.scan(TableName="list_snapshots")

    # Extrair os IDs dos snapshots
    snapshot_ids = [item["SnapshotId"]["S"] for item in response["Items"]]

    # Tentar excluir cada snapshot
    for snapshot_id in snapshot_ids:
        try:
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            print(f"Snapshot {snapshot_id} excluído com sucesso.")
        except Exception as e:
            print(f"Erro ao excluir o snapshot {snapshot_id}: {str(e)}")
            # Lidar com erros de exclusão, se necessário

    return {
        "statusCode": 200,
        "body": json.dumps("Processo de exclusão de snapshots concluído."),
    }
