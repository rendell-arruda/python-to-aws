import boto3
import json

dynamodb = boto3.client("dynamodb")
ec2 = boto3.client("ec2")


def lambda_handler(event, context):
    try:
        response = dynamodb.scan(TableName="list_snapshots")
        snapshots_to_delete = response.get("Items", [])

        for snapshot in snapshots_to_delete:
            snapshot_id = snapshot["SnapshotId"]["S"]
            try:
                ec2.delete_snapshot(SnapshotId=snapshot_id)
                dynamodb.delete_item(
                    TableName="list_snapshots", Key={"SnapshotId": {"S": snapshot_id}}
                )
                print(f"Snapshot {snapshot_id} excluído com sucesso.")
            except ec2.exceptions.ClientError as e:
                print(f"Erro ao excluir snapshot {snapshot_id}: {e}")
    except Exception as e:
        print(f"Erro ao escanear tabela DynamoDB: {e}")

    return {"statusCode": 200, "body": json.dumps("Snapshots excluídos com sucesso")}
