import boto3
import json

# Defina suas chaves de acesso e a lista de regiões
aws_access_key_id = "x"
aws_secret_access_key = "x"
region = "us-east-1"


def lambda_handler(instance_id, new_schedule_value):

    # Itera sobre cada região na lista de regiões
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region,
    )
    client = session.client("ec2")

    try:
        # Descreve a instância especificada
        response = client.describe_instances(InstanceIds=[instance_id])

        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                if instance["InstanceId"] == instance_id:
                    # Adiciona ou atualiza a tag "Schedule"
                    client.create_tags(
                        Resources=[instance_id],
                        Tags=[{"Key": "Schedule", "Value": new_schedule_value}],
                    )

                    print(
                        f"Instance {instance_id} schedule tag updated to {new_schedule_value}"
                    )

    except Exception as e:
        print(f"Error describing or updating instance {instance_id}: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps("Internal Server Error"),
        }


def get_input():
    try:
        # Solicita ao usuário para inserir o ID da instância
        instance_id = input("Enter the instance ID: ")

        # Solicita ao usuário para inserir o valor de agendamento
        input_value = input("Enter the schedule value: [1]running [2]stopped: ")

        # Converte o valor de entrada para um inteiro
        schedule_value = int(input_value)

        # Define o valor da tag com base na entrada do usuário
        if schedule_value == 1:
            new_schedule_value = "running"
            lambda_handler(instance_id, new_schedule_value)
        elif schedule_value == 2:
            new_schedule_value = "stopped"
            lambda_handler(instance_id, new_schedule_value)
        else:
            print("Invalid input! Please enter 1 or 2.")
            return

    except ValueError:
        print("Invalid input! Please enter a number (1 or 2).")
        return


if __name__ == "__main__":
    get_input()
