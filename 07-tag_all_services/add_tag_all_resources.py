import boto3

session = boto3.Session(profile_name='default')

client = session.client('resourcegroupstaggingapi')

# definir um metodo