import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
            Saldo:\t\tR$ {self.saldo:.2f}
        """


class ContaPoupanca(Conta):
    def __init__(self, numero, cliente, limite=1000, limite_saques=4):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/P:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
            Saldo:\t\tR$ {self.saldo:.2f}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    while True:
        print("\nSelecione a conta:")
        for i, conta in enumerate(cliente.contas):
            print(f"{i + 1} - {conta.__class__.__name__}: {conta.numero}")
        opcao = input("Digite o número da conta: ")

        try:
            indice = int(opcao) - 1
            if 0 <= indice < len(cliente.contas):
                return cliente.contas[indice]
            else:
                print("\n@@@ Opção inválida! @@@")
        except ValueError:
            print("\n@@@ Opção inválida! @@@")


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    print("Digite a opção do Tipo de conta para criar: Digite 1 para Conta corrente \nDigite 2 Para Conta Poupança \n")
    opcao = input() # Armazene a opção na variável 'opcao'

    if opcao == "1":
        conta_corrente = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
        contas.append(conta_corrente)
        cliente.contas.append(conta_corrente)
        print("\n=== Conta Corrente criada com sucesso! ===")
    elif opcao == "2":
        conta_poupanca = ContaPoupanca.nova_conta(cliente=cliente, numero=numero_conta)
        contas.append(conta_poupanca)
        cliente.contas.append(conta_poupanca)
        print("\n=== Conta Poupança criada com sucesso! ===")
    else:
        print("\n@@@ Opção inválida! @@@")
        return

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


main()

## Explicação do Código:
'''
O código está organizado em classes que representam as entidades do sistema bancário. 

**Classes Principais:**

* **Cliente:** 
    * Armazena informações básicas sobre o cliente, como nome, CPF, data de nascimento e endereço.
    * Possui uma lista de contas associadas ao cliente.
    * Define o método `realizar_transacao` para registrar transações em uma conta específica.

* **PessoaFisica:**
    * Subclasse de Cliente, representando um cliente pessoa física.
    * Herda as propriedades e métodos de Cliente.

* **Conta:**
    * Classe base para contas bancárias.
    * Possui atributos como número, agência, saldo e cliente.
    * Define métodos para sacar, depositar e acessar o histórico de transações.

* **ContaCorrente e ContaPoupanca:**
    * Subclasses de Conta, representando contas correntes e poupanças, respectivamente.
    * Possuem limites de saques e números máximos de saques específicos.
    * Sobrescrevem o método `sacar` para incluir validações adicionais.

* **Historico:**
    * Armazena o histórico de transações de uma conta.
    * Possui uma lista de transações e métodos para adicionar novas transações.

* **Transacao:**
    * Classe abstrata para representar uma transação bancária.
    * Define métodos abstratos para registrar uma transação.

* **Saque e Deposito:**
    * Subclasses de Transacao, representando saques e depósitos, respectivamente.
    * Implementam o método `registrar` para registrar a transação na conta.

**Fluxo do Código:**

1. O programa inicia a execução da função `main()`.
2. Um loop `while True` é executado até que o usuário escolha a opção "q" para sair do sistema.
3. A função `menu()` apresenta um menu de opções ao usuário.
4. De acordo com a opção escolhida, a função `main()` chama a função correspondente:
    * `depositar()`: Permite realizar depósitos em uma conta.
    * `sacar()`: Permite realizar saques em uma conta.
    * `exibir_extrato()`: Permite consultar o extrato de uma conta.
    * `criar_cliente()`: Permite criar um novo cliente.
    * `criar_conta()`: Permite criar uma nova conta para um cliente.
    * `listar_contas()`: Permite listar todas as contas criadas.
5. As funções específicas realizam as operações solicitadas, interagindo com as classes de dados e realizando as validações necessárias.

**Outras Funções:**

* **filtrar_cliente()**: Procura um cliente na lista de clientes pelo CPF.
* **recuperar_conta_cliente()**: Permite ao usuário escolher uma conta específica do cliente.

**Observações:**

* O código utiliza a biblioteca `textwrap` para formatar a saída do menu.
* A função `datetime.now()` é utilizada para registrar a data e hora das transações.
* O código inclui mensagens de erro para o usuário em caso de operações inválidas.
* As validações de dados, como CPF e data de nascimento, são simplificadas neste exemplo.
* O sistema não possui persistência de dados, ou seja, os dados são perdidos ao encerrar o programa.

Este código é um exemplo básico de um sistema bancário. Pode ser aprimorado com a adição de novas funcionalidades, como transferência entre contas, consulta de saldo, etc., além de implementar validações mais robustas e persistência de dados.

'''