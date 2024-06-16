import boto3
import json

# Lista de regiões onde as instâncias EC2 estão localizadas
regions = ["us-east-1", "sa-east-1"]


# Função principal que será executada
def lambda_handler(event, context):

    # Itera sobre cada região na lista de regiões
    for region in regions:
        # Cria uma sessão do boto3 com o perfil padrão
        session = boto3.Session(profile_name="default")

        # Cria um cliente EC2 para a região especificada
        client = session.client("ec2", region_name=region)

        try:
            # Descreve todas as instâncias EC2 na região especificada
            response = client.describe_instances()
            # Itera sobre cada reserva de instância na resposta
            for reservation in response["Reservations"]:
                # Itera sobre cada instância na reserva
                for instance in reservation["Instances"]:
                    # Obtém o ID da instância
                    instance_Id = instance["InstanceId"]

                    # Itera sobre as tags da instância, se existirem
                    for tag in instance.get("Tags", []):
                        # Verifica se a tag tem a chave "Schedule"
                        if tag["Key"] == "Schedule":
                            try:
                                # Solicita ao usuário para inserir um valor de agendamento
                                input_value = input(
                                    "Enter the schedule value: [1]running [2]stopped: "
                                )

                                # Converte o valor de entrada para um inteiro
                                input_value = int(input_value)

                                # Verifica se o valor de entrada é 1 (running)
                                if input_value == 1:
                                    # Cria ou atualiza a tag "Schedule" com o valor "running"
                                    client.create_tags(
                                        Resources=[instance_Id],
                                        Tags=[{"Key": "Schedule", "Value": "running"}],
                                    )
                                # Verifica se o valor de entrada é 2 (stopped)
                                elif input_value == 2:
                                    # Cria ou atualiza a tag "Schedule" com o valor "stopped"
                                    client.create_tags(
                                        Resources=[instance_Id],
                                        Tags=[{"Key": "Schedule", "Value": "stopped"}],
                                    )
                                else:
                                    # Imprime uma mensagem se a entrada for inválida
                                    print("Invalid input")

                            except Exception as e:
                                # Captura e imprime exceções durante o processamento da entrada do usuário
                                print(e)

        except Exception as e:
            # Captura e imprime exceções durante a descrição das instâncias
            print(f"Error describing instances: {str(e)}")
            return {
                "statusCode": 500,
                "body": json.dumps("Internal Server Error"),
            }


# Executa a função lambda_handler se o script for executado diretamente
if __name__ == "__main__":
    lambda_handler({}, {})
