import boto3
from datetime import datetime

dynamo = boto3.client('dynamodb')

# Verificar as tabelas
def lambda_handler(event, context):
    if 'TableName' not in event:
        raise Exception("No table name specified.")
    table_name = event['TableName']

    create_backup(table_name)

# Ciar o backup da tabela
def create_backup(table_name):
    print("Backing up table:", table_name)
    backup_name = table_name + '-' + datetime.now().strftime('%Y%m%d%H%M%S')

    response = dynamo.create_backup(
        TableName=table_name, BackupName=backup_name)

    print(f"Created backup {response['BackupDetails']['BackupName']}")