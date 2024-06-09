<h1 id='title'> AWS Lambda Multi-Account EC2 Instance Details</h1>

> Este projeto coleta detalhes das instâncias EC2 em várias contas da AWS e salva esses detalhes em um arquivo CSV que é então enviado para um bucket S3.

<!-- <img src="imagem.png" alt="Exemplo imagem"> -->

### Ajustes e melhorias

O projeto ainda está em desenvolvimento e as próximas atualizações serão voltadas nas seguintes tarefas:

- [ ] Adicionar mais tags de instância a serem coletadas.
- [ ] Melhorar o tratamento de erros.
- [ ] Adicionar suporte para mais regiões AWS.
- [ ] Criar uma interface para visualizar os dados coletados.

<h3>💻 Tecnologias envolvidas</h3>

![Amazon AWS](https://img.shields.io/badge/Amazon_AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 💻 Pré-requisitos

Antes de começar, certifique-se de atender aos seguintes requisitos:

- <b>AWS CLI</b> configurado e funcionando;
- <b>boto3</b> biblioteca Python instalada;
- Conta AWS com permissões adequadas configuradas;
- Permissões para a função Lambda assumida para os serviço STS, EC2, S3 e CloudWatch;
- Políticas de confiança configuradas corretamente nas contas alvo.

## 📁 Conteúdo
Este projeto inclui:

- lambda_function.py: Código principal da função Lambda.
- README.md: Este arquivo, explicando como configurar e usar o projeto.
  
## ☕ Usando o projeto
#### 1. Configurando a Função Lambda
##### 1.1 Crie a função Lambda:
- Acesse o Console da AWS Lambda.
- Crie uma nova função Lambda e carregue o código lambda_function.py.

##### 1.2. Configurar a Role da Lambda na conta principal:
Crie ou edite uma role do IAM para a Lambda com as seguintes permissões:

~~~json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "ec2:DescribeInstances",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "s3:PutObject",
                "s3:PutObjectAcl",
                "sts:AssumeRole"
            ],
            "Resource": [
                "arn:aws:iam::ACCOUNT_ID:role/ROLE_NAME",
                "arn:aws:iam::ACCOUNT_ID2:role/ROLE_NAME",
                "arn:aws:s3:::bucket_name/*"
            ]
        }
    ]
}
~~~
Substitua `arn:aws:iam::ACCOUNT_ID:role/ROLE_NAME` pelo ARN da role configurada.

##### 1.3 Configurar Políticas de Confiança na conta principal:
Para a conta de origem, adicione uma política de confiança permitindo que o lambda assuma a role:
~~~json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
~~~

##### 1.4 Configurar a Role da Lambda nas contas alvo:
Crie ou edite uma role do IAM para a Lambda com as seguintes permissões:

~~~json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "ec2:DescribeInstances",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "s3:PutObject",
                "s3:PutObjectAcl",
                "sts:AssumeRole"
            ],
            "Resource": "*"
        }
    ]
}
~~~

##### 1.5 Configurar Políticas de Confiança nas Contas Alvo:
Para cada role nas contas alvo, adicione uma política de confiança permitindo que a conta de origem assuma essa role:

~~~json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::ORIGIN_ACCOUNT_ID:root"
            },
            "Action": "sts:AssumeRole",
            "Condition":{}
        }
    ]
}

~~~
Substitua `ORIGIN_ACCOUNT_ID` pelo ID da conta onde a função Lambda está sendo executada.

#### 2. Executando a Função Lambda
- Acesse o Console da AWS Lambda;
- Teste a função Lambda fornecendo um evento de teste vazio;
- Verifique os logs no CloudWatch para garantir que a função está sendo executada corretamente;
- Verifique o bucket S3 configurado para ver se o arquivo CSV foi carregado corretamente.

## 📫 Contribuindo para o projeto

Para contribuir siga estas etapas:

1. Bifurque este repositório.
2. Crie um branch: `git checkout -b <nome_branch>`.
3. Faça suas alterações e confirme-as: `git commit -m '<mensagem_commit>'`
4. Envie para o branch original: `git push origin <nome_do_projeto> / <local>`
5. Crie a solicitação de pull.

Como alternativa, consulte a documentação do GitHub em [como criar uma solicitação pull](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## 📝 Licença

Esse projeto é de livre acesso e replicação, só pedimos que deem o credito devido caso ele seja usado de forma comercial, em redes sociais ou em quaisquer outras iniciativas.


<h3> 📫 Contribuindo para este projeto</h3>
<!---Se o seu README for longo ou se você tiver algum processo ou etapas específicas que deseja que os contribuidores sigam, considere a criação de um arquivo CONTRIBUTING.md separado--->
Para contribuir com projeto, siga estas etapas:

1. Bifurque este repositório.
2. Crie um branch: `git checkout -b <nome_branch>`.
3. Faça suas alterações e confirme-as: `git commit -m '<mensagem_commit>'`
4. Envie para o branch original: `git push origin <nome_do_projeto> / <local>`
5. Crie a solicitação de pull.

Como alternativa, consulte a documentação do GitHub em [como criar uma solicitação pull](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

[⬆ Voltar ao topo](#title)<br>
