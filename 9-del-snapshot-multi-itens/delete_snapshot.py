import json
import boto3

dynamodb = boto3.client("dynamodb")
ec2 = boto3.client("ec2")


def lambda_handler(event, context):
    # Recuperar os IDs dos snapshots armazenados no DynamoDB
    response = dynamodb.scan(TableName="list_snapshots")
    snapshots_to_delete = response.get("Items", [])

    for snapshot in snapshots_to_delete:
        snapshot_id = snapshot["SnapshotId"]["S"]
        region = snapshot["Region"]["S"]

        # Verificar se o snapshot ainda existe
        try:
            ec2.describe_snapshots(SnapshotIds=[snapshot_id])
            # O snapshot ainda existe, exclua-o
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            # Remova o item do DynamoDB após a exclusão
            dynamodb.delete_item(
                TableName="list_snapshots", Key={"SnapshotId": {"S": snapshot_id}}
            )
        except ec2.exceptions.ClientError as e:
            # Se o snapshot não existir mais, remova-o do DynamoDB
            if e.response["Error"]["Code"] == "InvalidSnapshot.NotFound":
                dynamodb.delete_item(
                    TableName="list_snapshots", Key={"SnapshotId": {"S": snapshot_id}}
                )
        except Exception as e:
            # Lidar com outros possíveis erros
            print(f"Erro ao excluir snapshot: {str(e)}")

    return {"statusCode": 200, "body": json.dumps("Código executado com sucesso")}
