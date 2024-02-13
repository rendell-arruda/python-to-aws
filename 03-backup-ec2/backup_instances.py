from datetime import datetime
import boto3


def lambda_handler(event, context):
    # Listando regioes
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName']
               for region in ec2_client.describe_regions()['Regions']]

    #passa em todas as regioes
    for region in regions:
        print('Instances in EC2 Region {0}:'.format(region))
        ec2 = boto3.resource('ec2', region_name=region)

        #procura com um filtro de tag
        instances = ec2.instances.filter(
            Filters=[
                {'Name': 'tag:backup', 'Values': ['true']}
            ]
        )

        # Adicionando timestamp data/mes/ano hh:min
        timestamp = datetime.utcnow().replace(microsecond=0).isoformat()

        for i in instances.all():
            for v in i.volumes.all():

                desc = 'Backup of {0}, volume {1}, created {2}'.format(
                    i.id, v.id, timestamp)
                print(desc)

                snapshot = v.create_snapshot(Description=desc)

                print("Created snapshot:", snapshot.id)