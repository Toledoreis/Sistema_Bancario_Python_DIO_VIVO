
# Simulação de Sistema Bancário em Python Base

Este programa em Python simula um sistema bancário simples com as seguintes funcionalidades:

- Depósito
- Saque
- Extrato
- Sair

## Funcionalidades:

- **Depósito:** Permite ao usuário depositar dinheiro em sua conta.
- **Saque:** Permite ao usuário sacar dinheiro de sua conta, respeitando um limite diário de valor e número de saques.
- **Extrato:** Exibe um histórico das transações realizadas (depósitos e saques).
- **Sair:** Encerra o programa.

## Limitações:

- O programa não possui um sistema de autenticação de usuários.
- As informações de saldo, extrato e número de saques são armazenadas em memória, ou seja, são perdidas quando o programa é encerrado.

## Como Usar:

1. **Execute o programa Python:**
   ```bash
   python desafio.py

**Siga as instruções do menu:**

- *Digite **d** para depositar.*
- *Digite **s** para sacar.*
- *Digite **e** para visualizar o extrato.*
- *Digite **q** para sair do programa.*
Exemplo de Uso:
```
- [d] Depositar
- [s] Sacar
- [e] Extrato
- [q] Sair
=> d

Informe o valor do depósito: 1000

Saldo: R$ 1000.00

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
=> s
Informe o valor do saque: 200

Saldo: R$ 800.00

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
=> e

================ EXTRATO ================
Depósito: R$ 1000.00
Saque: R$ 200.00

Saldo: R$ 800.00
==========================================

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
=> q
```