import locale


def formatar_para_real(valor: float) -> str:
    """Formata um valor float para o formato monetário brasileiro."""
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    valor_formatado = locale.format_string(
        '%.2f', float(valor), grouping=True)
    return valor_formatado


class Conta:
    LIMITE = 500
    LIMITE_SAQUES = 3

    def __init__(self, nome):
        self.nome = nome
        self.saldo = 0
        self.saques = 0
        self.extrato = []

    def depositar(self, valor: float) -> None:
        if valor <= 0:
            print('Valor inválido.')
            return
        self.saldo += valor
        valor_formatado = formatar_para_real(valor)
        self.extrato.append(f'Depósito: R${valor_formatado}')
        print(f'Depósito de R${valor_formatado} realizado com sucesso.')

    def sacar(self, valor: float) -> None:
        if valor <= 0:
            print('Valor inválido.')
            return
        if self.saques >= self.LIMITE_SAQUES:
            print('Limite de saques atingido.')
            return
        if self.saldo < valor:
            print('Saldo insuficiente.')
            return
        if valor > self.LIMITE:
            print('Valor acima do limite permitido.')
            return
        self.saldo -= valor
        self.saques += 1
        valor_formatado = formatar_para_real(valor)
        self.extrato.append(f'Saque: R${valor_formatado}')
        print(f'Saque de R${valor_formatado} realizado com sucesso.')

    def mostrar_extrato(self) -> None:
        if not self.extrato:
            print('Nenhuma operação realizada: o extrato está vazio.')
            return
        print('-'*40)
        print(f'Extrato de {self.nome}:')
        print('-'*40)
        for operacao in self.extrato:
            print(operacao)
        print('-'*40)
        print(f'Saldo atual: R${formatar_para_real(self.saldo)}')
        print('-'*40)


minha_conta = Conta('Gabriel')

print('Bem-vindo ao Banco Python.')

print(f"""{'-'*40}
Escolha a operação a ser realizada:
{'-'*40}
d - Depositar
s - Sacar
e - Extrato
q - Sair
{'-'*40}
""")

while True:
    operacao = input('Operação: ').lower().strip()
    match operacao:
        case 'd':
            valor = float(input('Digite o valor a ser depositado: R$'))
            minha_conta.depositar(valor)
        case 's':
            valor = float(input('Digite o valor a ser sacado: R$'))
            minha_conta.sacar(valor)
        case 'e':
            minha_conta.mostrar_extrato()
        case 'q':
            print('Programa encerrado.')
            break
        case _:
            print('Operação inválida.')
