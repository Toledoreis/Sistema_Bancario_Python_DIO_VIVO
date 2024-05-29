## Sistema Bancário Simples em Python

Este repositório contém um sistema bancário simples desenvolvido em Python. O sistema permite criar clientes, contas (corrente e poupança), realizar depósitos, saques e exibir extratos. 

### Funcionalidades:

* **Criar clientes:** Permite cadastrar novos clientes com nome, CPF, data de nascimento e endereço.
* **Criar contas:** Permite criar contas correntes e poupanças para clientes existentes, com limite de saques e valores.
* **Depositar:** Permite realizar depósitos em contas, registrando a transação no histórico da conta.
* **Sacar:** Permite realizar saques em contas, verificando o saldo, o limite de saques e o valor disponível.
* **Exibir extrato:** Permite visualizar o histórico de transações de uma conta, incluindo data, tipo de transação e valor.
* **Listar contas:** Permite listar todas as contas criadas no sistema.
* **Log de transações:** Registra todas as transações realizadas em um arquivo `log.txt`, com data, hora, nome da função, argumentos e resultado.

### Como usar:

1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/sistema-bancario-python.git
```

2. **Execute o script:**
```bash
python sistema_bancario.py
```

3. **Siga as instruções no menu:**
    * `d` - Depositar
    * `s` - Sacar
    * `e` - Extrato
    * `nc` - Nova conta
    * `lc` - Listar contas
    * `nu` - Novo usuário
    * `q` - Sair

### Observações:

* O sistema é simples e serve como um exemplo básico de implementação de um sistema bancário.
* As validações são mínimas e o foco está em apresentar os conceitos de orientação a objetos, abstração e gerenciamento de dados em Python.
* O sistema não utiliza banco de dados, as informações são armazenadas em memória durante a execução.

### Para melhorar o sistema:

* Implementar validações mais robustas para CPF, data de nascimento e valores.
* Criar um sistema de login e autenticação para os usuários.
* Utilizar um banco de dados para persistir os dados do sistema.
* Criar uma interface gráfica para tornar o sistema mais amigável.
* Adicionar funcionalidades como transferências entre contas, taxas e juros.

### Dicas:

* Leia a documentação do Python para entender melhor os conceitos utilizados no código.
* Experimente modificar o código para adicionar suas próprias funcionalidades.
* Use o depurador do Python para analisar o código e entender como ele funciona.

**Aproveite!** 
