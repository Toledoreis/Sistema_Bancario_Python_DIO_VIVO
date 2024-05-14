# Sistema Bancário em Python

Este programa em Python simula um sistema bancário simples, oferecendo as seguintes funcionalidades:

- Depósito
- Saque
- Extrato
- Criação de Usuários
- Criação de Contas
- Listagem de Contas

## Funcionalidades Detalhadas:

1. **Depósito:** Permite ao usuário depositar valores positivos em sua conta, atualizando o saldo e o extrato.

2. **Saque:** Permite ao usuário sacar dinheiro de sua conta, respeitando as seguintes regras:
   - Saldo suficiente para o saque.
   - Valor do saque dentro do limite por transação.
   - Número de saques dentro do limite diário.

3. **Extrato:** Exibe um histórico de todas as transações (depósitos e saques) realizadas na conta, além do saldo atual.

4. **Criar Usuário:** Permite a criação de novos usuários com informações como CPF, nome completo, data de nascimento e endereço. O sistema impede a criação de usuários com CPFs duplicados.

5. **Criar Conta:** Permite a criação de novas contas bancárias associadas a um usuário existente. Cada conta possui uma agência e um número de conta.

6. **Listar Contas:** Exibe uma lista de todas as contas bancárias criadas, mostrando a agência, o número da conta e o nome do titular.

## Estrutura do Código:

O código é organizado em funções para modularizar as funcionalidades do sistema:

- `menu()`: Exibe o menu de opções para o usuário.
- `depositar(...)`: Realiza operações de depósito.
- `sacar(...)`: Realiza operações de saque.
- `exibir_extrato(...)`: Exibe o extrato da conta.
- `criar_usuario(...)`: Gerencia a criação de novos usuários.
- `filtrar_usuario(...)`: Busca um usuário pelo CPF.
- `criar_conta(...)`: Cria uma nova conta bancária.
- `listar_contas(...)`: Lista as contas existentes.
- `main()`: Função principal que coordena a execução do programa.



## Como Executar:

Para executar este programa, você precisa ter o Python instalado em seu computador. Se você ainda não o possui, pode baixá-lo em [https://www.python.org/downloads/](https://www.python.org/downloads/).

Siga estas etapas para executar o programa:

1. **Salve o código:** Copie o código fornecido e cole-o em um editor de texto. Salve o arquivo com a extensão `.py`. Por exemplo, você pode salvar o arquivo como `desafio.py`.

2. **Abra um terminal ou prompt de comando:**
   - No Windows: Pressione a tecla Windows, digite "cmd" e pressione Enter.
   - No macOS: Abra o aplicativo Terminal em "Aplicativos" > "Utilitários".
   - No Linux: A forma de abrir o terminal varia de acordo com a distribuição, mas geralmente você pode encontrá-lo no menu de aplicativos.

3. **Navegue até o diretório do arquivo:** Use o comando `cd` para navegar até o diretório onde você salvou o arquivo `desafio.py`. Por exemplo, se você salvou o arquivo na pasta "Documentos", digite o seguinte comando no terminal:
   ```bash
   cd Documentos

**Execute o programa:**

- *Digite o seguinte comando e pressione Enter:*

```bash
python desafio.py
```

Utilizando o Menu: Após executar o programa, você verá o seguinte menu de opções:

```bash
================ MENU ================
 [d]	Depositar
 [s]	Sacar
 [e]	Extrato
 [nc]	Nova conta
 [lc]	Listar contas
 [nu]	Novo usuário
 [q]	Sair
 =>
```
Para usar o programa, digite a letra correspondente à operação que você deseja realizar e pressione Enter. 
*Por exemplo:*
- Digite 'd' e pressione Enter para realizar um depósito. O programa solicitará o valor do depósito.
- Digite 's' e pressione Enter para realizar um saque. O programa solicitará o valor do saque.
- Digite 'e' e pressione Enter para visualizar o extrato da sua conta.
- Digite 'nc' para criar uma nova conta. O programa solicitará as informações do usuário.
- Digite 'lc' para listar as contas existentes.
- Digite 'nu' para criar um novo usuário. O programa solicitará as informações do usuário.
- Digite 'q' e pressione Enter para sair do programa.
O programa irá guiá-lo pelas etapas de cada operação.