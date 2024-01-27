import boto3


def lambda_handler(event, context):

    # Listar as regioes
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName']
               for region in ec2_client.describe_regions()['Regions']]

    # Buscar em todas as regioes
    for region in regions:
        ec2 = boto3.resource('ec2', region_name=region)

        print("Region:", region)

        # Filtrar somente as instancias Desligadas
        instances = ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name',
                      'Values': ['stopped']}])

        # Iniciar as Instancias
        for instance in instances:
            instance.start()
            print('Started instance: ', instance.id)