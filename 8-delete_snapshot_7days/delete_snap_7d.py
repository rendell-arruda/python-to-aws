# import boto3
# from datetime import datetime, timedelta, timezone

# config = boto3.session.Config(connect_timeout=300, read_timeout=300)


# def listar_snapshots_com_paginacao(regions):
#     # percorre as regioes
#     for region in regions:
#         print(f"##### {region} #####")

#         # para cada regiao abrir uma session e um client
#         session = boto3.Session(profile_name="default")
#         ec2 = session.client("ec2", region_name=region, config=config)

#         ##### SNAPSHOTS ######
#         # iniciar a paginacao para snapshot
#         paginator = ec2.get_paginator("describe_snapshots")
#         snapshot_iterator = paginator.paginate(OwnerIds=["self"])

#         # Iterar sobre as paginas
#         for page in snapshot_iterator:
#             snapshots = page["Snapshots"]

#             snapshots_linked_ami = []
#             snapshots_can_delete = []

#             for snapshot in snapshots:

#                 # Verifica se o snap esta em uso por uma ami
#                 response = ec2.describe_images(
#                     Filters=[
#                         {
#                             "Name": "block-device-mapping.snapshot-id",
#                             "Values": [snapshot["SnapshotId"]],
#                         }
#                     ]
#                 )

#                 if len(response["Images"]) == 0:
#                     # O snapshot não está em uso por uma AMI, verifica se foi criado há mais de 7 dias
#                     data_criacao = snapshot["StartTime"].replace(tzinfo=timezone.utc)
#                     data_atual = datetime.now(timezone.utc)

#                     diferenca = data_atual - data_criacao

#                     if diferenca.days > 2:
#                         # O snapshot foi criado há mais de 7 dias, pode ser excluído
#                         # print(f"Excluindo snapshot {snapshot['SnapshotId']}\n")
#                         snapshots_can_delete.append(snapshot["SnapshotId"])
#                         # ec2.delete_snapshot(SnapshotId=snapshot[ 'SnapshotId'])
#                     else:
#                         # O snapshot foi criado há menos de 7 dias, não pode ser excluído
#                         # print(
#                         #     "O snapshot ",
#                         #     {snapshot["SnapshotId"]},
#                         #     "foi criado há menos de 7 dias e não pode ser excluído\n",
#                         # )
#                         snapshots_linked_ami.append(snapshot["SnapshotId"])
#                 else:
#                     # O snapshot está em uso por uma AMI, não pode ser excluído
#                     # print(
#                     #     "O snapshot",
#                     #     snapshot["SnapshotId"],
#                     #     "está em uso por uma AMI e não pode ser excluído\n",
#                     # )
#                     snapshots_linked_ami.append(snapshot["SnapshotId"])

#         # Imprime a lista de snapshots que não foram excluídos
#         print(
#             "Snapshots que não podem ser excluidos",
#             len(snapshots_linked_ami),
#             "São eles:",
#             snapshots_linked_ami,
#             "\n",
#         )
#         print(
#             "Snapshot que tem mais de 3 dias e podem ser excluidos",
#             len(snapshots_can_delete),
#             "São eles:",
#             snapshots_can_delete,
#             "\n",
#         )


# # Lista de regiões
# regions = ["us-east-1", "sa-east-1"]

# # Chama a função para listar snapshots com paginação
# listar_snapshots_com_paginacao(regions)

import boto3
from datetime import datetime, timedelta, timezone

config = boto3.session.Config(connect_timeout=300, read_timeout=300)


def lambda_handler(event, context):
    regions = ["us-east-1", "sa-east-1"]

    # Chama a função para listar snapshots com paginação
    for region in regions:
        print(f"##### {region} #####")

        # para cada regiao abrir uma session e um client
        session = boto3.Session()
        ec2 = session.client("ec2", region_name=region, config=config)

        ##### SNAPSHOTS ######
        # iniciar a paginacao para snapshot
        paginator = ec2.get_paginator("describe_snapshots")
        snapshot_iterator = paginator.paginate(OwnerIds=["self"])

        # Iterar sobre as paginas
        for page in snapshot_iterator:
            snapshots = page["Snapshots"]

            snapshots_linked_ami = []
            snapshots_can_delete = []

            for snapshot in snapshots:

                # Verifica se o snap esta em uso por uma ami
                response = ec2.describe_images(
                    Filters=[
                        {
                            "Name": "block-device-mapping.snapshot-id",
                            "Values": [snapshot["SnapshotId"]],
                        }
                    ]
                )

                if len(response["Images"]) == 0:
                    # O snapshot não está em uso por uma AMI, verifica se foi criado há mais de 7 dias
                    data_criacao = snapshot["StartTime"].replace(tzinfo=timezone.utc)
                    data_atual = datetime.now(timezone.utc)

                    diferenca = data_atual - data_criacao

                    if diferenca.days > 2:
                        # O snapshot foi criado há mais de 7 dias, pode ser excluído
                        # print(f"Excluindo snapshot {snapshot['SnapshotId']}\n")
                        snapshots_can_delete.append(snapshot["SnapshotId"])
                        # ec2.delete_snapshot(SnapshotId=snapshot[ 'SnapshotId'])
                    else:
                        # O snapshot foi criado há menos de 7 dias, não pode ser excluído
                        # print(
                        #     "O snapshot ",
                        #     {snapshot["SnapshotId"]},
                        #     "foi criado há menos de 7 dias e não pode ser excluído\n",
                        # )
                        snapshots_linked_ami.append(snapshot["SnapshotId"])
                else:
                    # O snapshot está em uso por uma AMI, não pode ser excluído
                    # print(
                    #     "O snapshot",
                    #     snapshot["SnapshotId"],
                    #     "está em uso por uma AMI e não pode ser excluído\n",
                    # )
                    snapshots_linked_ami.append(snapshot["SnapshotId"])

            # Imprime a lista de snapshots que não foram excluídos
            print(
                "Snapshots que não podem ser excluídos",
                len(snapshots_linked_ami),
                "São eles:",
                snapshots_linked_ami,
                "\n",
            )
            print(
                "Snapshot que tem mais de 3 dias e podem ser excluídos",
                len(snapshots_can_delete),
                "São eles:",
                snapshots_can_delete,
                "\n",
            )


# Chamada para fins de teste no VS Code
if __name__ == "__main__":
    lambda_handler({}, {})
