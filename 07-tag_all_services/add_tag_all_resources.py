import boto3


def lambda_handler(event, context):
    regions = ["us-east-1", "sa-east-1", "us-east-2"]

    # percorrer todas as regioes da contas
    for region in regions:
        try:
            # Cria uma sessão com a AWS, usando o perfil e a região definidos anteriormente
            session = boto3.Session(profile_name="default")
            # Cria um cliente para o serviço Resource Groups Tagging API
            client = session.client("resourcegroupstaggingapi", region_name=region)

            print(f"entrando na regiao {region}")

            # defini quais tags serao adicionadas
            tag_key = "test3"
            tag_value = "taguieidenovo"

            paginator = client.get_paginator("get_resources")
            get_resources = paginator.paginate()

            # Percorre todos os recursos retornados pelo método get_resources
            for page in get_resources:
                for resource in page["ResourceTagMappingList"]:
                    # obtem o arn do recurso
                    resource_arn = resource["ResourceARN"]
                    print(resource_arn)

                    # Obtém as tags do recurso. Se o recurso não tiver tags, retorna uma lista vazia.
                    tags = resource.get("Tags", [])

                    # verifica se o recurso não possui a tag específica e não possui outras tags, ele adicionará
                    if not any(tag["Key"] == tag_key for tag in tags):
                        response = client.tag_resources(
                            ResourceARNList=[resource_arn], Tags={tag_key: tag_value}
                        )
                        print(f"O resource {resource_arn} foi tagueado")
                    else:
                        print(f"O resource {resource_arn} já possui a tag")
                    print("\n")

        # Captura qualquer exceção que ocorra durante o processamento e imprime na tela a mensagem de erro.
        except Exception as e:
            print(f"Exceção na região {region}: {e}")


# para teste no vs code
if __name__ == "__main__":
    lambda_handler({}, {})
