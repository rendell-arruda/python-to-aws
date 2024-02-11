<h1 id='title'>🐍 Python for AWS Course</h1>

> Este repositório contém os projetos desenvolvidos no Curso de Python para AWS com 5 scripts para automatizar a criação de recursos e tarefas na nuvem da Amazon utilizando Lambda Functions. O curso faz parte da Comunidade Revolução Cloud, comandada pelo grande André Iacono, da qual eu participo.
 
<h3>💻 Tecnologias envolvidas</h3>

![Amazon AWS](https://img.shields.io/badge/Amazon_AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)


<h3> 📁 Conteúdo</h3>
Os projetos foram divididos nas seguintes aulas:

- [x] Script 1 - EC2 e Lambda: criação de instâncias;
- [x] Script 2 - Upload de arquivos no S3: 
- [x] Script 3 - Backup/snapshot de instâncias EC2;
- [x] Script 4 - EC2 On e Off: agendamento de on e off via Cloudwatch e EventBridge;
- [x] Script 5 - DynamoDb;
- [x] Script 6 - Delete EBS no attached with conditional tag

<h3> ☕ Usando as Lambdas Functions</h3>

Para usar cada script siga estas etapas:

 1. Crie uma função lambda selecionando em <b>"Runtime"</b> qual versão de python você gostaria de usar - recomendo Python 3.9;
 2. Em permissões crie uma new role com permissões básicas de Lambda - Por default sua Lambda function virá com permissões apenas para o CloudWatch;
 3. Na aba <b>"Configuration"</b> escolha a opção <b>"Permissions"</b>, clique na role name criada.
 4. Edite a Permission Policy na console do IAM adicionando as permissões necessárias conforme seu objetivo. Cada pasta desse projeto possui uma sugestão de IAM role;
 5. Voltando ao painel da Lambda function cole na aba <b>Code</b> o código python disponibilizado no projeto;
 6. Vai trabalhar com variáveis? Edite suas variáveis na aba <b>Configuration</b> opção <b>Environment variables</b>;
 7. Ao terminar de editar seu código clique em deploy para finalizar;
 8. Se você chegou nessa etapa você pode testar sua função Lambda clicando em <b>Test</b>;
 9. Adicionalmente você pode conferir a execução da sua Lambda function pelos logs do CloudWatch.


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
