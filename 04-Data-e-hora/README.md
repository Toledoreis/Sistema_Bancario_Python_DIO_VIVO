## Sistema Bancário Simples em Python

Este repositório contém um sistema bancário simples implementado em Python, permitindo aos usuários realizar operações básicas como depósitos, saques, extratos e gerenciar clientes e contas.

### Funcionalidades:

* **Criar Clientes:** Permite criar novos clientes (pessoas físicas) com nome, data de nascimento, CPF e endereço.
* **Criar Contas:** Permite criar contas correntes e poupanças, associando-as a clientes existentes.
* **Depositar:** Permite realizar depósitos em contas existentes.
* **Sacar:** Permite realizar saques em contas existentes, com validação de saldo, limite e número de saques.
* **Exibir Extrato:** Permite visualizar o extrato de uma conta, exibindo as transações realizadas e o saldo atual.
* **Listar Contas:** Permite listar todas as contas criadas, exibindo seus detalhes.

### Como Executar:

1. Clone este repositório: `git clone https://github.com/seu-usuario/sistema-bancario-python.git`
2. Navegue para a pasta do projeto: `cd sistema-bancario-python`
3. Execute o script: `python main.py`

### Estrutura do Código:

O código é organizado em classes que representam os conceitos do sistema bancário:

* **`Cliente`:** Classe base para clientes, com endereço e lista de contas.
* **`PessoaFisica`:** Classe que representa um cliente pessoa física, herdando de `Cliente`.
* **`Conta`:** Classe base para contas bancárias, com saldo, número, agência, cliente e histórico de transações.
* **`ContaCorrente`:** Classe para contas correntes, com limite de crédito e limite de saques.
* **`ContaPoupanca`:** Classe para contas poupanças, com limite de crédito e limite de saques.
* **`Historico`:** Classe que armazena o histórico de transações de uma conta.
* **`Transacao`:** Classe abstrata para representar transações, com métodos para registrar e obter o valor.
* **`Saque`:** Classe que representa um saque, herdando de `Transacao`.
* **`Deposito`:** Classe que representa um depósito, herdando de `Transacao`.

### Observações:

* O código utiliza a biblioteca `abc` para definir classes abstratas e a biblioteca `datetime` para lidar com datas e horários.
* A função `log_transacao` é um decorador que registra as transações realizadas.
* A função `menu` exibe o menu de opções para o usuário.
* O código utiliza listas para armazenar os clientes e contas criados.

