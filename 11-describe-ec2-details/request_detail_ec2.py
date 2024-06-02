import boto3
import csv

session = boto3.Session(profile_name="default")

# Crie um cliente EC2
ec2_client = session.client("ec2")

# Descreva instâncias EC2
response = ec2_client.describe_instances()

# Lista para armazenar detalhes das instâncias
instances_details = []

# Iterar sobre todas as reservas e instâncias
for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        # Pegar o ID da instância
        instance_id = instance["InstanceId"]

        # Pegar o tipo da instância
        instance_type = instance["InstanceType"]

        # Pegar a plataforma (Linux/UNIX ou Windows)
        platform = instance.get(
            "Platform", "Linux/UNIX"
        )  # Platform key is only present for Windows instances

        # Pegar o nome da instância (tag Name)
        name = None
        for tag in instance.get("Tags", []):
            if tag["Key"] == "Name":
                name = tag["Value"]
                break

        # Adicionar os detalhes da instância na lista
        instances_details.append(
            {
                "Instance ID": instance_id,
                "Instance Type": instance_type,
                "Name": name,
                "Platform": platform,
            }
        )

# Escrever os detalhes das instâncias em um arquivo CSV
csv_file = "ec2_instances.csv"
csv_columns = ["Instance ID", "Instance Type", "Name", "Platform"]

try:
    with open(csv_file, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in instances_details:
            writer.writerow(data)
except IOError:
    print("I/O error")

print(f"Detalhes das instâncias EC2 foram salvos no arquivo {csv_file}")
