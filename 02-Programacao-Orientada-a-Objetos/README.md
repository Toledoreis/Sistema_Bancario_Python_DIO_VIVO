## Este repositório contém um sistema bancário simples em Python. O sistema permite criar clientes, contas correntes e poupanças, realizar depósitos, saques e consultar extratos.

**Funcionalidades:**

* **Criar Clientes:** Permite criar novos clientes com nome, CPF, data de nascimento e endereço.
* **Criar Contas:** Permite criar contas correntes e poupanças para clientes existentes.
* **Depositar:** Permite realizar depósitos em contas existentes.
* **Sacar:** Permite realizar saques em contas existentes, com validação de saldo, limite e número de saques.
* **Extrato:** Permite consultar o extrato de uma conta, mostrando as transações realizadas.
* **Listar Contas:** Permite listar todas as contas criadas no sistema.

**Como Usar:**

1. Execute o arquivo `main.py`.
2. O sistema mostrará um menu com as opções disponíveis.
3. Selecione a opção desejada e siga as instruções.

**Código:**

O código está organizado em classes para representar as entidades do sistema, como clientes, contas e transações.

* **Cliente:** Representa um cliente do banco, com nome, CPF, data de nascimento e endereço.
* **PessoaFisica:** Subclasse de Cliente para representar clientes pessoas físicas.
* **Conta:** Classe base para contas bancárias, com número, agência, saldo e cliente.
* **ContaCorrente:** Subclasse de Conta, com limite de saque e número máximo de saques.
* **ContaPoupanca:** Subclasse de Conta, com limite de saque e número máximo de saques.
* **Historico:** Classe para armazenar o histórico de transações de uma conta.
* **Transacao:** Classe abstrata para representar uma transação bancária.
* **Saque:** Subclasse de Transacao, representa um saque em uma conta.
* **Deposito:** Subclasse de Transacao, representa um depósito em uma conta.

**Exemplos de Uso:**

* Para criar um novo cliente, selecione a opção "nu" no menu.
* Para criar uma conta corrente, selecione a opção "nc" no menu.
* Para realizar um depósito, selecione a opção "d" no menu.
* Para realizar um saque, selecione a opção "s" no menu.
* Para consultar o extrato, selecione a opção "e" no menu.

**Observações:**

* O sistema usa uma estrutura de lista para armazenar clientes e contas.
* As validações de CPF, data de nascimento e endereço não estão implementadas no código.
* O sistema não salva os dados persistidos, ou seja, os dados são perdidos ao encerrar o programa.
* As funcionalidades do sistema foram implementadas de forma simples para estudos.
* Foi usado o IA Studio da Google como apoio
* Bootcamp de Python com IA



