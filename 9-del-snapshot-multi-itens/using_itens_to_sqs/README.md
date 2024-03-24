# Documentação do Serviço AWS Lambda - Listagem e Exclusão de Snapshots

---

## Objetivo

Este serviço AWS Lambda é composto por dois lambdas que trabalham em conjunto para listar e, em seguida, excluir snapshots de volumes EBS na AWS. O primeiro lambda lista os snapshots de acordo com critérios específicos e armazena seus IDs em uma tabela DynamoDB. O segundo lambda recebe esses IDs da tabela DynamoDB e exclui os snapshots correspondentes.

## Primeiro Lambda - Listagem de Snapshots

### Função `lambda_handler(event, context)`

Esta função é responsável por listar os snapshots de volumes EBS em regiões específicas da AWS e armazenar seus IDs em uma tabela do DynamoDB.

#### Parâmetros:

- `event`: O objeto de evento que aciona a função Lambda. Neste caso, não é usado.
- `context`: O contexto de execução da função Lambda. Neste caso, não é usado.

#### Retorno:

- Um dicionário contendo o código de status HTTP e uma mensagem de sucesso.

#### Fluxo de Funcionamento:

1. Inicializa o cliente SQS dentro da função.
2. Define as regiões onde os snapshots serão listados.
3. Itera sobre cada região e executa o seguinte procedimento:
   - Lista os snapshots utilizando o cliente EC2.
   - Itera sobre os snapshots listados.
   - Calcula a diferença entre o tempo atual e o tempo de criação de cada snapshot.
   - Armazena o ID dos snapshots que atendem aos critérios de idade em uma tabela do DynamoDB.
   - Envia o token de paginação para uma fila SQS para processamento adicional.
4. Retorna um objeto de resposta HTTP com o status 200 e uma mensagem indicando que os snapshots foram listados com sucesso e o token de paginação foi enviado para a fila SQS.

## Segundo Lambda - Exclusão de Snapshots

### Função `lambda_handler(event, context)`

Esta função é responsável por receber mensagens da fila SQS contendo os IDs dos snapshots a serem excluídos, consultar a tabela DynamoDB para obter esses IDs e, em seguida, excluir os snapshots correspondentes.

#### Parâmetros:

- `event`: O objeto de evento que aciona a função Lambda. Neste caso, não é usado.
- `context`: O contexto de execução da função Lambda. Neste caso, não é usado.

#### Retorno:

- Um dicionário contendo o código de status HTTP e uma mensagem indicando que os snapshots foram excluídos com sucesso.

#### Fluxo de Funcionamento:

1. Importa o módulo boto3 e define o cliente SQS dentro da função.
2. Recebe a mensagem do SQS para obter o próximo token de paginação.
3. Consulta a tabela DynamoDB usando o próximo token.
4. Itera sobre os snapshots obtidos e executa o seguinte procedimento:
   - Exclui o snapshot utilizando o cliente EC2.
   - Remove o item correspondente da tabela DynamoDB.
   - Registra o sucesso ou falha da operação de exclusão.
5. Retorna um objeto de resposta HTTP com o status 200 e uma mensagem indicando que os snapshots foram excluídos com sucesso.

## Dependências Externas:

- `boto3`: Biblioteca da AWS SDK para Python que fornece acesso aos serviços da AWS.
- `json`: Biblioteca padrão do Python para manipulação de dados JSON.

## Variáveis Globais:

- `sqs_queue_url`: URL da fila SQS onde serão recebidas as mensagens contendo os próximos tokens de paginação.
- `dynamodb`: Cliente do DynamoDB para interação com a tabela contendo os IDs dos snapshots.
- `ec2`: Cliente do EC2 para listar e excluir snapshots.

## Observações:

- Certifique-se de configurar corretamente as permissões necessárias para que os lambdas acessem os serviços SQS, DynamoDB e EC2.
- Este serviço assume que os IDs dos snapshots a serem excluídos estão armazenados na tabela do DynamoDB.
- As mensagens na fila SQS devem conter os próximos tokens de paginação para que o segundo lambda possa processar os snapshots correspondentes.
- É importante tratar adequadamente os erros que possam ocorrer durante o processamento das mensagens do SQS e a exclusão dos snapshots.

--- 
