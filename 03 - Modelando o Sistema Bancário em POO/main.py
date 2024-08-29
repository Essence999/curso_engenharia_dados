from abc import ABC, abstractmethod
from datetime import datetime


class Cliente:
    def __init__(self, endereco: str):
        self.endereco: str = endereco
        self.contas: list = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome: str = nome
        self.cpf: str = cpf
        self.data_nascimento: datetime = data_nascimento


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero: int = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)

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
            print('Saldo insuficiente.')
            return
        elif valor > 0:
            self._saldo -= valor
            print(f'Saque de R${valor:.2f} realizado com sucesso.')
            return True
        else:
            print('Valor inválido.')
            return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f'Depósito de R${valor:.2f} realizado com sucesso.')
        else:
            print('Valor inválido.')
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.
             transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        execedeu_limite_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print('Limite de saque excedido.')
        elif execedeu_limite_saques:
            print('Limite de saques excedido.')
        else:
            return super().sacar(valor)
        return False

    def __str__(self) -> str:
        return f"""\
            Agência: {self.agencia}
            Conta: {self.numero}
            Titular: {self.cliente.nome}
        """


class Historico():
    def __init__(self):
        self._transacoes = []

    @ property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }
        )


class Transacao(ABC):
    @ property
    @ abstractmethod
    def valor(self):
        pass

    @classmethod
    @ abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @ property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @ property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def menu():
    print('Bem-vindo ao Banco Python.')
    print(f"""{'-'*40}
Escolha a operação a ser realizada:
{'-'*40}
d - Depositar
s - Sacar
e - Extrato
nc - Nova conta
lc - Listar contas
nu - Novo usuário
q - Sair
{'-'*40}
""")


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [
        cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print('Cliente não possui contas.')
        return
    return cliente.contas[0]


def depositar(clientes):
    cpf = input('Digite o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado.')
        return

    valor = float(input('Digite o valor a ser depositado: '))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        print('Conta não encontrada.')
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input('Digite o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado.')
        return

    valor = float(input('Digite o valor a ser sacado: '))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        print('Conta não encontrada.')
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input('Digite o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado.')
        return

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        print('Conta não encontrada.')
        return

    print('-'*40)
    print('Extrato:')
    print('-'*40)
    transacoes = conta.historico.transacoes

    extrato = ""

    if not transacoes:
        extrato = "Nenhuma transação registrada."
    else:
        for transacao in transacoes:
            extrato += f"""\
            {transacao['tipo']}: R${transacao['valor']:.2f}
            """
    print(extrato)
    print(f'Saldo atual: R${conta.saldo:.2f}')
    print('-'*40)


def criar_cliente(clientes):
    cpf = input('Digite o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print('Cliente já cadastrado.')
        return

    nome = input('Digite o nome do cliente: ')
    data_nascimento = input('Digite a data de nascimento do cliente: ')
    endereco = input('Digite o endereço do cliente: ')

    cliente = PessoaFisica(
        nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    print('Cliente cadastrado com sucesso.')


def criar_conta(numero_conta, clientes, contas):
    cpf = input('Digite o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado.')
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    print('Conta criada com sucesso.')


def listar_contas(contas):
    for conta in contas:
        print('-'*40)
        print(conta)
        print('-'*40)


def main():
    clientes = []
    contas = []

    menu()

    while True:
        operacao = input('Operação: ').lower().strip()

        match operacao:
            case 'd':
                depositar(clientes)
            case 's':
                sacar(clientes)
            case 'e':
                exibir_extrato(clientes)
            case 'nu':
                criar_cliente(clientes)
            case 'nc':
                numero_conta = len(contas) + 1
                criar_conta(numero_conta, clientes, contas)
            case 'lc':
                listar_contas(contas)
            case 'q':
                print('Programa encerrado.')
                break
            case _:
                print('Operação inválida.')


main()
