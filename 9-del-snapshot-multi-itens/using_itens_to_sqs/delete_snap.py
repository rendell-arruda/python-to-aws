import boto3
import json

sqs_queue_url = "https://sqs.us-east-1.amazonaws.com/266549158321/fila_snap_sqs"

sqs = boto3.client("sqs")
ec2 = boto3.client("ec2")


def lambda_handler(event, context):
    # Variável para armazenar o número de snapshots excluídos com sucesso
    deleted_snapshots_count = 0

    # Loop para processar continuamente as mensagens da fila SQS
    while True:
        # Recebe mensagens da fila SQS
        response = sqs.receive_message(QueueUrl=sqs_queue_url, MaxNumberOfMessages=10)
        if "Messages" in response:
            for message in response["Messages"]:
                # Analisa o corpo da mensagem
                body = json.loads(message["Body"])
                snapshot_id = body["snapshot_id"]

                # Define o número máximo de tentativas de processamento para cada mensagem
                max_attempts = 1
                attempts = 0

                while attempts < max_attempts:
                    try:
                        # Exclui a snapshot
                        ec2.delete_snapshot(SnapshotId=snapshot_id)
                        # Incrementa o contador de snapshots excluídos com sucesso
                        deleted_snapshots_count += 1
                        # Exclui a mensagem da fila
                        sqs.delete_message(
                            QueueUrl=sqs_queue_url,
                            ReceiptHandle=message["ReceiptHandle"],
                        )
                        break
                    except Exception as e:
                        # Se ocorrer uma exceção, imprime o erro e tenta novamente
                        print(
                            f"Tentativa {attempts+1} de excluir snapshot {snapshot_id}: {e}"
                        )
                        attempts += 1

                if attempts == max_attempts:
                    # Se não for possível excluir a snapshot após o número máximo de tentativas, exclui a mensagem da fila
                    print(
                        f"Não foi possível excluir snapshot {snapshot_id} após {max_attempts} tentativas. Excluindo mensagem da fila."
                    )
                    sqs.delete_message(
                        QueueUrl=sqs_queue_url, ReceiptHandle=message["ReceiptHandle"]
                    )

        else:
            # Se não houver mais mensagens na fila, sai do loop
            break

    # Exibe o número de snapshots excluídos com sucesso
    print(f"Total de snapshots excluídos com sucesso: {deleted_snapshots_count}")
    return {
        "statusCode": 200,
        "body": json.dumps(
            f"Total de snapshots excluídos com sucesso: {deleted_snapshots_count}"
        ),
    }
