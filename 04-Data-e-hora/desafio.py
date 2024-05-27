import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class ContasIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""\
            Agência:\t{conta.agencia}
            Número:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
            Saldo:\t\tR$ {conta.saldo:.2f}
        """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        self.indice_conta = 0

    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 2:
            print("\n@@@ Você excedeu o número de transações permitidas para hoje! @@@")
            return

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

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
                yield transacao

# Filtragem de todas as trasações diarias

def transacoes_do_dia(self):
        data_atual = datetime.utcnow().date()
        transacoes = []
        for transacao in self._transacoes:
            data_transacao = datetime.strptime(
                transacao["data"], "%d-%m-%Y %H:%M:%S"
            ).date()
            if data_atual == data_transacao:
                transacoes.append(transacao)
        return transacoes



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

def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f"{datetime.now()}: {func.__name__.upper()}")
        return resultado

    return envelope

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

@log_transacao
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

@log_transacao
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

@log_transacao
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
    extrato = ""
    tem_transacao = False
    for transacao in conta.historico.gerar_relatorio():
        tem_transacao = True
        extrato += f"\n{transacao['data']}\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    if not tem_transacao:
        extrato = "Não foram realizadas movimentações"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

@log_transacao
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

@log_transacao
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    print("Selecione a opção desejada para criar sua conta:\nDigite 1 para Conta Corrente; \nDigite 2 Para Conta Poupança.")
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
    
@log_transacao
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
Este código Python implementa um sistema bancário simples que permite aos usuários realizar operações como depósitos, saques, extratos e criação de contas e clientes. Vamos analisar o código passo a passo, explicando cada classe, função e conceito importante:

**1. Importações:**

```python
import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
```

* `textwrap`:  Utiliza a função `textwrap.dedent` para formatar texto e remover espaços em branco do início de cada linha.
* `abc`: A biblioteca `abc` (Abstract Base Classes) é usada para definir classes abstratas, que são classes que não podem ser instanciadas diretamente, mas podem servir como modelos para outras classes.
* `datetime`:  É utilizada para trabalhar com datas e horários.

**2. Classe `ContasIterador`:**

```python
class ContasIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""\
            Agência:\t{conta.agencia}
            Número:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
            Saldo:\t\tR$ {conta.saldo:.2f}
        """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1
```

* Esta classe implementa a iteração sobre uma lista de contas.
* O método `__init__` inicializa o iterador com a lista de contas e define o índice inicial para 0.
* `__iter__` retorna o próprio objeto, tornando-o iterável.
* `__next__` retorna a próxima conta formatada como uma string, incrementando o índice. Se o índice ultrapassar o limite da lista, `StopIteration` é levantado.

**3. Classe `Cliente`:**

```python
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        self.indice_conta = 0

    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 2:
            print("\n@@@ Você excedeu o número de transações permitidas para hoje! @@@")
            return

        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)
```

* Representa um cliente do banco.
* `__init__` inicializa um cliente com um endereço e uma lista vazia de contas.
* `realizar_transacao`:  Verifica se o cliente excedeu o limite de transações diárias e, se não, registra a transação na conta.
* `adicionar_conta`:  Adiciona uma conta à lista de contas do cliente.

**4. Classe `PessoaFisica`:**

```python
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
```

* Representa um cliente do tipo pessoa física, herdando da classe `Cliente`.
* Adiciona atributos específicos para pessoa física: `nome`, `data_nascimento` e `cpf`.

**5. Classe `Conta`:**

```python
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
```

* Classe base para contas bancárias.
* `__init__` inicializa uma conta com um número, um cliente e um saldo inicial de 0.
* `nova_conta`:  Método de classe para criar novas contas.
* `saldo`, `numero`, `agencia`, `cliente`, `historico`:  Propriedades (getters) para acessar os atributos privados da conta.
* `sacar`:  Efetua um saque, verificando se o saldo é suficiente.
* `depositar`:  Efetua um depósito, verificando se o valor é válido.

**6. Classe `ContaCorrente`:**

```python
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
```

* Representa uma conta corrente, herdando de `Conta`.
* Adiciona atributos para limite de crédito e limite de saques.
* Sobrescreve o método `sacar` para verificar o limite de crédito e o número de saques.
* `__str__`:  Define como uma conta corrente será representada como uma string.

**7. Classe `ContaPoupanca`:**

```python
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
```

* Representa uma conta poupança, herdando de `Conta`.
* Semelhante à conta corrente, com seus próprios limites e sobrescrita do método `sacar`.
* `__str__`:  Define como uma conta poupança será representada como uma string.

**8. Classe `Historico`:**

```python
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

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
                yield transacao
```

* Armazena o histórico de transações de uma conta.
* `__init__` inicializa o histórico com uma lista vazia de transações.
* `transacoes`:  Propriedade para acessar as transações.
* `adicionar_transacao`:  Adiciona uma transação ao histórico.
* `gerar_relatorio`:  Gera um iterador sobre as transações, permitindo filtrar por tipo de transação.

**9. Classe `Transacao` (abstrata):**

```python
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass
```

* Classe abstrata para representar uma transação, definindo métodos que devem ser implementados pelas subclasses.
* `valor`:  Propriedade abstrata que deve retornar o valor da transação.
* `registrar`:  Método abstrata que deve registrar a transação em uma conta.

**10. Classe `Saque`:**

```python
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
```

* Representa um saque, herdando de `Transacao`.
* Implementa `valor` e `registrar`, realizando o saque e adicionando a transação ao histórico da conta.

**11. Classe `Deposito`:**

```python
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
```

* Representa um depósito, herdando de `Transacao`.
* Implementa `valor` e `registrar`, realizando o depósito e adicionando a transação ao histórico da conta.

**12. Função `log_transacao` (decorador):**

```python
def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f"{datetime.now()}: {func.__name__.upper()}")
        return resultado

    return envelope
```

* Decorador que registra o nome da função e o horário de execução.
* É usado para registrar as chamadas de funções que realizam transações.

**13. Função `menu`:**

```python
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
```

* Exibe o menu de opções para o usuário.

**14. Função `filtrar_cliente`:**

```python
def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None
```

* Filtra a lista de clientes por CPF.

**15. Função `recuperar_conta_cliente`:**

```python
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
```

* Permite que o usuário escolha uma conta de um cliente, exibindo a lista de contas.

**16. Função `depositar` (decorada com `log_transacao`):**

```python
@log_transacao
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)
```

* Permite que o usuário realize um depósito em uma conta, verificando se o cliente e a conta existem.

**17. Função `sacar` (decorada com `log_transacao`):**

```python
@log_transacao
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
```

* Permite que o usuário realize um saque em uma conta, verificando se o cliente e a conta existem.

**18. Função `exibir_extrato` (decorada com `log_transacao`):**

```python
@log_transacao
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
    extrato = ""
    tem_transacao = False
    for transacao in conta.historico.gerar_relatorio():
        tem_transacao = True
        extrato += f"\n{transacao['data']}\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    if not tem_transacao:
        extrato = "Não foram realizadas movimentações"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")
```

* Permite que o usuário visualize o extrato de uma conta, mostrando as transações e o saldo.

**19. Função `criar_cliente` (decorada com `log_transacao`):**

```python
@log_transacao
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
```

* Permite que o usuário crie um novo cliente, solicitando os dados necessários.

**20. Função `criar_conta` (decorada com `log_transacao`):**

```python
@log_transacao
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    print("Selecione a opção desejada para criar sua conta:\nDigite 1 para Conta Corrente; \nDigite 2 Para Conta Poupança.")
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
```

* Permite que o usuário crie uma nova conta (corrente ou poupança), associando-a a um cliente existente.

**21. Função `listar_contas` (decorada com `log_transacao`):**

```python
@log_transacao
def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))
```

* Lista todas as contas criadas, exibindo os detalhes de cada conta.

**22. Função `main`:**

```python
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
```

* Função principal do programa que inicia o loop do menu, processando as opções escolhidas pelo usuário.

**Observações:**

* O código usa listas (`clientes`, `contas`) para armazenar os objetos criados.
* A função `log_transacao` é um decorador que registra as transações.
* As funções de `depositar`, `sacar`, `exibir_extrato`, `criar_cliente` e `criar_conta` usam a função `filtrar_cliente` para encontrar o cliente correto.
* A função `recuperar_conta_cliente` permite que o usuário escolha a conta do cliente.
* O loop `while True` no `main` continua a execução do programa até que o usuário escolha a opção "q" para sair.

**Em resumo, o código implementa um sistema bancário simples com as seguintes funcionalidades:**

* Criar clientes (pessoas físicas)
* Criar contas (correntes e poupanças)
* Realizar depósitos
* Realizar saques
* Exibir extratos
* Listar contas

Este código serve como um bom exemplo de como utilizar classes, herança, métodos, propriedades e decoradores em Python para criar um sistema simples com funcionalidade básica.
'''