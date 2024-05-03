import boto3
import json


def lambda_handler(event, context):
    regions = ["us-east-1", "sa-east-1"]

    # percorrer todas as regiões da conta
    for region in regions:
        try:
            print(f"Entrando na região ### {region} ###")
            # Cria uma sessão com a AWS, usando o perfil e a região definidos anteriormente
            # session = boto3.Session(profile_name="default")
            # Cria um cliente para o serviço Resource Groups Tagging API
            client = boto3.client("resourcegroupstaggingapi", region_name=region)

            # Defini quais tags serão adicionadas
            tag_key = "map-migrated"
            tag_value_new = "migAgorafoi2"
            tag_value_old = "mig23769"

            paginator = client.get_paginator("get_resources")
            get_resources = paginator.paginate()

            # Percorre todos os recursos retornados pelo método get_resources
            for page in get_resources:
                for resource in page.get("ResourceTagMappingList", []):
                    resource_arn = resource.get("ResourceARN")
                    if resource_arn:
                        # Obtém as tags do recurso. Se o recurso não tiver tags, retorna uma lista vazia.
                        tags = resource.get("Tags", [])

                        # Verifica se o recurso não possui a tag específica e não possui outras tags,
                        # ele adicionará com o valor novo.
                        if not any(tag["Key"] == tag_key for tag in tags):
                            try:
                                response = client.tag_resources(
                                    ResourceARNList=[resource_arn],
                                    Tags={tag_key: tag_value_new},
                                )
                                print(
                                    f"O resource {resource_arn} foi tagueado com {tag_value_new}"
                                )
                            except Exception as tag_error:
                                print(
                                    f"Exceção ao taguear {resource_arn} com {tag_value_new}: {tag_error}"
                                )
                        # Se o recurso possui a key específica e o valor antigo, retagueia com o novo valor.
                        elif any(
                            tag["Key"] == tag_key and tag["Value"] == tag_value_old
                            for tag in tags
                        ):
                            try:
                                response = client.tag_resources(
                                    ResourceARNList=[resource_arn],
                                    Tags={tag_key: tag_value_new},
                                )
                                print(
                                    f"O resource {resource_arn} foi retagueado com {tag_value_new}"
                                )
                            except Exception as tag_error:
                                print(
                                    f"Exceção ao retaguear {resource_arn} com {tag_value_new}: {tag_error}"
                                )
                        else:
                            print(
                                f"O resource {resource_arn} já possui a tag com outro valor"
                            )
                        print("\n")

        # Captura qualquer exceção que ocorra durante o processamento e imprime na tela a mensagem de erro.
        except Exception as e:
            print(f"Exceção na região {region}: {e}")

    # TODO implement
    return {"statusCode": 200, "body": json.dumps("Hello from Lambda!")}
