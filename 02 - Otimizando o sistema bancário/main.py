def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f'Depósito: R${valor:.2f}\n'
        print(f'Depósito de R${valor:.2f} realizado com sucesso.')
    else:
        print('Valor inválido.')
    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_limite_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print('Saldo insuficiente.')
    elif excedeu_limite:
        print('Valor acima do limite permitido.')
    elif excedeu_limite_saques:
        print('Limite de saques atingido.')
    elif valor > 0:
        saldo -= valor
        extrato += f'Saque: R${valor:.2f}\n'
        numero_saques += 1
        print(f'Saque de R${valor:.2f} realizado com sucesso.')
    else:
        print('Valor inválido.')
    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print('-'*40)
    print('Extrato:')
    print('-'*40)
    print(extrato)
    print(f'Saldo atual: R${saldo:.2f}')
    print('-'*40)


def criar_usuario(usuarios):
    cpf = input('Digite o CPF do usuário: ')
    usuario = filtrar_usuarios(cpf, usuarios)

    if usuario:
        print('Usuário já cadastrado.')
        return

    nome = input('Digite o nome do usuário: ')
    data_nascimento = input('Digite a data de nascimento do usuário: ')
    endereco = input('Digite o endereço do usuário: ')

    usuarios.append({"nome": nome, "cpf": cpf,
                    "data_nascimento": data_nascimento, "endereco": endereco})
    print('Usuário cadastrado com sucesso.')


def filtrar_usuarios(cpf, usuarios):
    usuarios_filtrados = [
        usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input('Digite o CPF do usuário: ')
    usuario = filtrar_usuarios(cpf, usuarios)

    if usuario:
        print('Conta criada com sucesso.')
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print('Usuário não encontrado.')


def listar_contas(contas):
    for contas in contas:
        print('-'*40)
        print(f"Agência: {conta['agencia']}")
        print(f"Número da conta: {conta['numero_conta']}")
        print(f"Titular: {conta['usuario']['nome']}")
        print('-'*40)


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

LIMITE_SAQUES = 3
AGENCIA = "0001"

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
usuarios = []
contas = []


while True:
    operacao = input('Operação: ').lower().strip()
    match operacao:
        case 'd':
            valor = float(input('Digite o valor a ser depositado: R$'))
            saldo, extrato = depositar(saldo, valor, extrato)

        case 's':
            valor = float(input('Digite o valor a ser sacado: R$'))
            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )
        case 'e':
            exibir_extrato(saldo, extrato=extrato)
        case 'nu':
            criar_usuario(usuarios)
        case 'nc':
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
        case 'lc':
            listar_contas(contas)
        case 'q':
            print('Programa encerrado.')
            break
        case _:
            print('Operação inválida.')
