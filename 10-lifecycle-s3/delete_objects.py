import boto3
from datetime import (
    datetime,
    timedelta,
    timezone,
)  # Importa as bibliotecas necessárias para manipulação de datas


def delete_objects(bucket_name, prefix, days):
    # Inicializa o cliente S3
    s3 = boto3.client("s3")

    # Calcula a data de corte com base no número de dias fornecidos
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

    # Lista de objetos a serem excluídos
    objects_to_delete = []

    # Pagina os resultados da listagem de objetos para o bucket e prefixo especificados
    paginator = s3.get_paginator("list_objects_v2")
    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

    # Itera sobre as páginas de resultados
    for page in page_iterator:
        # Verifica se há objetos na página atual
        if "Contents" in page:
            # Itera sobre os objetos na página atual
            for obj in page["Contents"]:
                # Obtém a chave (nome do objeto) e a data de modificação do objeto
                key = obj["Key"]
                last_modified = obj["LastModified"].replace(tzinfo=timezone.utc)

                # Verifica se a data de modificação é anterior à data de corte
                if last_modified < cutoff_date:
                    # Adiciona o objeto à lista de objetos a serem excluídos
                    objects_to_delete.append({"Key": key})

    # Se houver objetos a serem excluídos, realiza a exclusão
    if len(objects_to_delete) > 0:
        s3.delete_objects(Bucket=bucket_name, Delete={"Objects": objects_to_delete})
        print(f"{len(objects_to_delete)} objects deleted.")
    else:
        print("No objects found to delete.")


def lambda_handler(event, context):
    # Parâmetros para a função delete_objects
    bucket_name = "devops-mind"  # Nome do bucket S3
    prefix = "tshoot-incidente-alb/AWSLogs/"  # Prefixo dos objetos a serem excluídos
    days = 2  # Número de dias antes da data atual para considerar objetos como candidatos à exclusão

    # Chama a função delete_objects com os parâmetros especificados
    delete_objects(bucket_name, prefix, days)
