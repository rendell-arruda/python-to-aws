import boto3
import csv
import json

session = boto3.Session(profile_name="default")

# Crie um cliente EC2
ec2_client = session.client("ec2")

# Descreva instâncias EC2
response = ec2_client.describe_instances()

# Lista para armazenar detalhes das instâncias
instances_details = []

# Iterar sobre todas as respostas [Reservations]
for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:

        # Pegar os detalhes da instância
        instance_id = instance["InstanceId"]
        # Pegar o estado da instância
        instance_state = instance["State"]["Name"]

        # pegar o nome da instância
        name = None  # Inicializa a variável name
        for tag in instance.get("Tags", []):
            if tag["Key"] == "Name":
                name = tag["Value"]
                break
        # pegar a tag Schedule
        schedule = None
        for tag in instance.get("Tags", []):
            if tag["Key"] == "Schedule":
                schedule = tag["Value"]
                break

        # Adiciona os detalhes da instancia  na lista
        instances_details.append(
            {
                "Instance Id": instance_id,
                "Instance State": instance_state,
                "Name": name,
                "Schedule": schedule,
            }
        )


# SALVAR OS DADOS EM DIFERENTES FORMATOS
####
# especificar o nome do arquivo de saida em jSON
json_file = "ec2_details.json"
## Salvar a saída do codigo no arquivo txt
with open(json_file, "w") as f:
    json.dump(instances_details, f, indent=4)
####

# especificar o nome do arquivo de saida em csv
csv_file = "ec2_instances.csv"
csv_columns = ["Instance Id", "Instance State", "Name", "Schedule"]

try:
    with open(csv_file, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in instances_details:
            writer.writerow(data)
except IOError:
    print("Erro de E/S")

print(f"Detalhes das instâncias EC2 foram salvos nos arquivos {json_file} e {csv_file}")

## enviar os dados para o S3
# Enviar o arquivo CSV para um bucket S3
s3_client = session.client("s3")
bucket_name = "ilustredev-ec2-details-bucket"
s3_key = "details/ec2_instances.csv"

try:
    s3_client.upload_file(csv_file, bucket_name, s3_key)
    print(
        f"Arquivo {csv_file} foi enviado para o bucket S3 {bucket_name} com a chave {s3_key}."
    )
except Exception as e:
    print(f"Erro ao enviar o arquivo para o bucket S3: {e}")
