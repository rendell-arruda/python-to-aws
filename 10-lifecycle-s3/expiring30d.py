import boto3

# Inicializa o cliente S3
s3_client = boto3.client("s3")


# Função para aplicar a configuração do ciclo de vida do bucket
def put_bucket_lifecycle_configuration(bucket_name):
    # Configuração do ciclo de vida
    lifecycle_configuration = {
        "Rules": [
            {
                "ID": "Expiring30d",  # Identificador da regra
                "Expiration": {"Days": 1},  # Expira objetos após 30 dias
                "Prefix": "",  # Aplica a regra a todos os objetos do bucket
                "Status": "Enabled",  # Ativa a regra
            },
        ]
    }

    try:
        # Aplica a configuração do ciclo de vida ao bucket especificado
        s3_client.put_bucket_lifecycle_configuration(
            Bucket=bucket_name, LifecycleConfiguration=lifecycle_configuration
        )
        print(f"Policy applied successfully to bucket: {bucket_name}")
    except Exception as e:
        print(f"Error applying policy to bucket {bucket_name}: {e}")


# Função para listar os buckets e aplicar a configuração do ciclo de vida
def list_buckets():
    try:
        # Lista os buckets
        buckets = s3_client.list_buckets()
        # Itera sobre os buckets encontrados
        for bucket in buckets["Buckets"]:
            bucket_name = bucket["Name"]
            # Aplica a configuração do ciclo de vida para cada bucket
            put_bucket_lifecycle_configuration(bucket_name)
            # print(bucket)  # Exibe informações do bucket (opcional)
    except Exception as e:
        print(f"Error listing buckets: {e}")


# Chama a função para listar os buckets e aplicar a configuração do ciclo de vida
list_buckets()
