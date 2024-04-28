LifecycleConfiguration = {
    "Rules": [
        {
            # Configuração para expiração de objetos
            "Expiration": {
                "Date": datetime(
                    2015, 1, 1
                ),  # Data específica para expiração (opcional)
                "Days": 123,  # Número de dias após os quais o objeto expira (opcional)
                "ExpiredObjectDeleteMarker": True
                | False,  # Define se o marcador de exclusão será criado quando o objeto expirar (opcional)
            },
            "ID": "string",  # Identificador único da regra (obrigatório)
            "Prefix": "string",  # Define se o marcador de exclusão será criado quando o objeto expirar (opcional)
            "Filter": {  # Filtro para aplicar a regra apenas a objetos específicos (opcional)
                "Prefix": "string",  # Prefixo dos objetos (opcional)
                "Tag": {  # Filtro por tag (opcional)
                    "Key": "string",  # Chave da tag
                    "Value": "string",  # Valor da tag
                },
                "ObjectSizeGreaterThan": 123,  # Filtra objetos com tamanho maior que o especificado (opcional)
                "ObjectSizeLessThan": 123,  # Filtra objetos com tamanho menor que o especificado (opcional)
                "And": {  # Combinação de filtros com operador AND (opcional)
                    "Prefix": "string",  # Prefixo dos objetos (opcional)
                    "Tags": [  # Lista de tags (opcional)
                        {
                            "Key": "string",  # Chave da tag
                            "Value": "string",  # Valor da tag
                        },
                    ],
                    "ObjectSizeGreaterThan": 123,  # Filtra objetos com tamanho maior que o especificado (opcional)
                    "ObjectSizeLessThan": 123,  # Filtra objetos com tamanho menor que o especificado (opcional)
                },
            },
            "Status": "Enabled" | "Disabled",  # Status da regra (obrigatório)
            "Transitions": [  # Transições de classe de armazenamento (opcional)
                {
                    "Date": datetime(
                        2015, 1, 1
                    ),  # Data específica para a transição (opcional)
                    "Days": 123,  # Número de dias após os quais a transição ocorre (opcional)
                    "StorageClass": "GLACIER"
                    | "STANDARD_IA"
                    | "ONEZONE_IA"
                    | "INTELLIGENT_TIERING"
                    | "DEEP_ARCHIVE"
                    | "GLACIER_IR",  # Classe de armazenamento para a transição (obrigatório)
                },
            ],
            "NoncurrentVersionTransitions": [  # Transições de versões não atuais (opcional)
                {
                    "NoncurrentDays": 123,  # Número de dias após os quais a transição ocorre (obrigatório)
                    "StorageClass": "GLACIER"
                    | "STANDARD_IA"
                    | "ONEZONE_IA"
                    | "INTELLIGENT_TIERING"
                    | "DEEP_ARCHIVE"
                    | "GLACIER_IR",  # Classe de armazenamento para a transição (obrigatório)
                    "NewerNoncurrentVersions": 123,  # Número de versões mais recentes não atuais a serem excluídas (opcional)
                },
            ],
            "NoncurrentVersionExpiration": {  # Expiração de versões não atuais (opcional)
                "NoncurrentDays": 123,  # Número de dias após os quais a versão não atual expira (obrigatório)
                "NewerNoncurrentVersions": 123,  # Número de versões mais recentes não atuais a serem excluídas (opcional)
            },
            "AbortIncompleteMultipartUpload": {  # Abortar uploads multipartes incompletos (opcional)
                "DaysAfterInitiation": 123  # Número de dias após a iniciação do upload multipart para abortar (obrigatório)
            },
        },
    ]
}
