import json
import boto3

from datetime import datetime, timedelta, timezone

config = boto3.session.Config(connect_timeout=300, read_timeout=300)


def lambda_handler(event, context):
    regions = ["us-east-1", "sa-east-1"]
    days_created = 0

    # Chama a função para listar snapshots com paginação
    for region in regions:
        print(f"##### {region} #####")

        # para cada regiao abrir uma session e um client
        # session = boto3.Session()
        ec2 = boto3.client("ec2", region_name=region, config=config)

        ##### SNAPSHOTS ######
        # iniciar a paginacao para snapshot
        paginator = ec2.get_paginator("describe_snapshots")
        snapshot_iterator = paginator.paginate(OwnerIds=["self"])

        # Iterar sobre as paginas
        for page in snapshot_iterator:
            snapshots = page["Snapshots"]

            snapshots_can_delete = []

            for snapshot in snapshots:

                data_criacao = snapshot["StartTime"].replace(tzinfo=timezone.utc)
                data_atual = datetime.now(timezone.utc)

                diferenca = data_atual - data_criacao

                if diferenca.days >= days_created:
                    # O snapshot foi criado há mais de X dias, pode ser excluído
                    snapshots_can_delete.append(snapshot["SnapshotId"])
                    print(f"Excluindo snapshot {snapshot['SnapshotId']}\n")

                    ##COMENTARIO DE DELEÇAO DE SNAP
                    try:

                        ec2.delete_snapshot(SnapshotId=snapshot["SnapshotId"])
                    except Exception as e:
                        print(e)
                else:
                    # O snapshot foi criado há menos de X dias, não pode ser excluído
                    print(
                        f"O snapshot ",
                        {snapshot["SnapshotId"]},
                        "foi criado há menos de ",
                        days_created,
                        "dias e não pode ser excluído\n",
                    )

            # Imprime a lista de snapshots que não foram excluídos

            print(
                "Qtdd de Snapshot que tem mais de",
                days_created,
                "dias e podem ser excluídos,",
                len(snapshots_can_delete),
                "são eles:",
                snapshots_can_delete,
                "\n",
            )
    return {"statusCode": 200, "body": json.dumps("Codigo executado com sucesso")}


# para teste no VS Code
if __name__ == "__main__":
    lambda_handler({}, {})
