import boto3  # Importa a biblioteca Boto3 para interagir com os serviços AWS

# Configurar a sessão do boto3
session = boto3.Session(profile_name="default")  # Cria uma sessão Boto3 usando o perfil AWS configurado como "default"

# Inicializar o cliente AWS Budgets
budgets_client = session.client('budgets')  # Inicializa o cliente AWS Budgets para poder fazer chamadas à API do serviço

# Função para criar um orçamento com um alerta
def create_budget_with_alert(account_id, budget_name, budget_amount, email_address):
    try:
        response = budgets_client.create_budget(  # Chama o método create_budget para criar um novo orçamento
            AccountId=account_id,  # ID da conta AWS onde o orçamento será criado
            Budget={
                'BudgetName': budget_name,  # Nome do orçamento
                'BudgetLimit': {
                    'Amount': str(budget_amount),  # Limite do orçamento convertido para string
                    'Unit': 'USD'  # Unidade monetária (USD)
                },
                'CostFilters': {},  # Filtros de custo (vazio neste caso)
                'CostTypes': {  # Tipos de custo a serem incluídos no orçamento
                    'IncludeTax': True,
                    'IncludeSubscription': True,
                    'UseBlended': False,
                    'IncludeRefund': False,
                    'IncludeCredit': False,
                    'IncludeUpfront': True,
                    'IncludeRecurring': True,
                    'IncludeOtherSubscription': True,
                    'IncludeSupport': True,
                    'IncludeDiscount': True,
                    'UseAmortized': False
                },
                'TimeUnit': 'MONTHLY',  # Unidade de tempo para o orçamento (mensal)
                'TimePeriod': {  # Período de tempo para o orçamento
                    'Start': '2024-07-01T00:00:00Z',  # Data de início do orçamento (em formato ISO 8601)
                    'End': '2025-07-01T00:00:00Z'  # Data de término do orçamento (em formato ISO 8601)
                },
                'BudgetType': 'COST'  # Tipo de orçamento (baseado em custos)
            },
            NotificationsWithSubscribers=[
                {
                    'Notification': {  # Configuração da notificação
                        'NotificationType': 'ACTUAL',  # Tipo de notificação (baseado em valores reais)
                        'ComparisonOperator': 'GREATER_THAN',  # Operador de comparação (maior que)
                        'Threshold': 80.0,  # Limite de alerta (80% do orçamento)
                        'ThresholdType': 'PERCENTAGE',  # Tipo de limite (percentual)
                        'NotificationState': 'ALARM'  # Estado da notificação (alarme)
                    },
                    'Subscribers': [
                        {
                            'SubscriptionType': 'EMAIL',  # Tipo de subscrição (email)
                            'Address': email_address  # Endereço de email para receber notificações
                        }
                    ]
                }
            ]
        )
        print(f'Orçamento {budget_name} criado com sucesso!')  # Mensagem de sucesso na criação do orçamento
    except Exception as e:  # Captura qualquer exceção que ocorra
        print(f'Erro ao criar o orçamento: {e}')  # Exibe mensagem de erro caso ocorra uma exceção

# Exemplo de uso
account_id = '266549158321'  # Substitua pelo ID da sua conta AWS
budget_name = 'MeuOrcamentoMensal'  # Substitua pelo nome do orçamento desejado
budget_amount = 5  # Substitua pelo valor do orçamento desejado
email_address = 'rendellarruda3@gmail.com'  # Substitua pelo seu endereço de email

create_budget_with_alert(account_id, budget_name, budget_amount, email_address)  # Chama a função para criar o orçamento com alerta
