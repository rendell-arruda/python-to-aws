import boto3


def lambda_handler(event, context):
    regions = ["us-east-1", "sa-east-1", "us-east-2"]

    # percorrer todas as regiões da conta
    for region in regions:
        try:
            # Cria uma sessão com a AWS, usando o perfil e a região definidos anteriormente
            session = boto3.Session(profile_name="default")
            # Cria um cliente para o serviço Resource Groups Tagging API
            client = session.client("resourcegroupstaggingapi", region_name=region)

            print(f"Entrando na região {region}")

            # Defini quais tags serão adicionadas
            tag_key = "tagueadoEm2"
            tag_value = "07h20"

            paginator = client.get_paginator("get_resources")
            get_resources = paginator.paginate()

            # Percorre todos os recursos retornados pelo método get_resources
            for page in get_resources:
                for resource in page.get("ResourceTagMappingList", []):
                    # Obtem o ARN do recurso
                    resource_arn = resource.get("ResourceARN")
                    if resource_arn:
                        # Obtém as tags do recurso. Se o recurso não tiver tags, retorna uma lista vazia.
                        tags = resource.get("Tags", [])

                        # Verifica se o recurso não possui a tag específica e não possui outras tags, ele adicionará
                        if not any(tag["Key"] == tag_key for tag in tags):
                            try:
                                response = client.tag_resources(
                                    ResourceARNList=[resource_arn],
                                    Tags={tag_key: tag_value},
                                )
                                print(f"O resource {resource_arn} foi tagueado")
                            except Exception as tag_error:
                                print(f"Exceção ao taguear {resource_arn}: {tag_error}")
                        else:
                            print(f"O resource {resource_arn} já possui a tag")
                        print("\n")

        # Captura qualquer exceção que ocorra durante o processamento e imprime na tela a mensagem de erro.
        except Exception as e:
            print(f"Exceção na região {region}: {e}")


# para teste no VS Code
if __name__ == "__main__":
    lambda_handler({}, {})
