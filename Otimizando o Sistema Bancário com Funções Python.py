'''
Objetivo Geral

Separar as funções existentes de saque, depósito e extrato em funções.
Criar duas novas funções: cadastrar usuário(cliente) e cadastrar conta bancária.

Separar funções

Devemos criar funções para todas as operações do sistema. Para exercitar tudo o que aprendemos
neste módulo, cada função vai ter uma regra na passagem de argumentos. O retorno e a forma 
como serão chamadas, pode ser definida por você da forma que achar melhor.

A função saque deve receber os argumentos apenas por nome(keyword only). Sugestão de argumentos: saldo, valor,
extrato, limite, numero_saques, limite_saques. Sugestão de retorno: saldo extrato.

Novas funções 

Precisamos criar duas novas funções: criar usuário e criar conta corrente.
Fique a vontade para adicionar mais funções, exemplo: listar contas.

Criar usuário deve armazenar os usuários em uma lista, um usuário é composto
por: nome, data de nascimento, cpf e endereço. O endereço é uma string com o formato:
logradouro, nro - bairro - cidade/sigla estado. deve ser armazenado somente os números
do CPF. Não podemos cadastrar 2 usuários com o mesmo CPF.

Criar conta corrente 

O programa deve armazenar contas em uma lista, uma conta é
composta por: agência, número da conta, usuário. O número
da conta é sequencial, iniciado em 1. O número da agência
é fixo: "0001". O usuário pode ter mais de uma conta, mas uma
conta pertence a somente um usuário.


'''
def leiaFloat(msg):
    while True:
        try:
            n = float(input(msg))
            if n > 0:
                return n
            else:
                print("Insira um valor positivo!")
        except (ValueError, TypeError):
            print('\033[0;31;40mERRO: por favor, digite um número válido.\033[m')
        except KeyboardInterrupt:
            print('\n\033[0;31;40mUsuário preferiu não digitar esse número.\033[m')
            return 0

def linha(tam=42):
    return '-' * tam

def cabeçalho(txt):
    print(linha())
    print(txt.center(42))
    print(linha())

def Menu1(lista):
    cabeçalho("Menu Primário")
    for item in lista:
        print(item)
    print(linha())
    opcao = input("Selecione uma opção:")
    if opcao in ["a", "b", "c", "q"]:
        return opcao
    else:
        print("Digite um valor válido!")

def Menu2(lista):
    cabeçalho("Menu Secundário")
    for item in lista:
        print(item)
    print(linha())
    opcao = input("Selecione uma opção:")
    if opcao in ["d", "s", "e", "q"]:
        return opcao
    else:
        print("Digite um valor válido!")

def realizar_deposito(saldo, valor, extrato, /):
    saldo += valor
    extrato.append(valor)
    cabeçalho("Depósito Realizado com sucesso!")
    return saldo

def realizar_saque(*, saldo, valor, extrato, numero_saque, limite_saque):
    if numero_saque >= LIMITE_SAQUES:
        print('Você já realizou o número máximo de Saques')
    elif valor > limite_saque:
        print(f'Não é permitido realizar um saque maior que R$ {limite_saque}')
    elif saldo < valor:
        print("Saldo insuficiente para realizar o saque!")
    else:
        saldo -= valor
        extrato.append(-valor)
        numero_saque += 1
        cabeçalho("Saque realizado com sucesso!")
    return saldo, extrato, numero_saque

def Extrato(saldo, *, demonstrativo):
    cabeçalho("Extrato")
    for valor in demonstrativo:
        print(f'R$ {valor:.2f}')
    print(f'Saldo: R$ {saldo:.2f}')

def criar_usuário(lista_usuario):
    cpf = input("Informe o CPF (somente números): ")
    if any(usuario["cpf"] == cpf for usuario in lista_usuario):
        print("Já existe usuário com esse CPF!")
        return

    nome = input("Insira o seu nome completo: ").strip()
    nascimento = input("Data de nascimento (dd/mm/aaaa): ")
    logradouro = input("Logradouro: ")
    numero = input("Número: ")
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    estado = input("Estado (sigla): ")

    endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{estado}"
    usuario = {"nome": nome, "nascimento": nascimento, "cpf": cpf, "endereco": endereco}
    lista_usuario.append(usuario)
    print("Usuário criado com sucesso!")

def criar_conta_corrente(lista_usuarios, lista_contas):
    cpf = input("Informe o CPF (somente números): ")
    usuario_encontrado = None
    for usuario in lista_usuarios:
        if usuario["cpf"] == cpf:
            usuario_encontrado = usuario
            break

    if usuario_encontrado:
        print("CPF identificado")
        numero_conta = len(lista_contas) + 1
        conta = {
            "agencia": "0001",
            "numero_conta": numero_conta,
            "usuario": usuario_encontrado,
            "saldo": 0,
            "extrato": [],
            "numero_saques": 0
        }
        lista_contas.append(conta)
        print(f"Conta criada com sucesso! Número da conta: {numero_conta}")
    else:
        print("Usuário não encontrado.")
        return None

def selecionar_conta(contas):
    if not contas:
        print("Nenhuma conta cadastrada.")
        return None

    for i, conta in enumerate(contas, start=1):
        nome = conta["usuario"]["nome"]
        print(f"{i}. Conta {conta['numero_conta']} - {nome}")
    try:
        indice = int(input("Selecione o número da conta: ")) - 1
        if 0 <= indice < len(contas):
            return contas[indice]
        else:
            print("Índice inválido.")
    except ValueError:
        print("Entrada inválida.")
    return None

c_usuario = []
c_contas = []
extrato = []
Saldo = 0
limite = 500.00
número_saques = 0
LIMITE_SAQUES = 3

while True:
    resposta = Menu1(["a - Criar um usuário", "b - Criar uma conta corrente", "c - Acessar operações bancárias", "q - Sair"])
    if resposta == "a":
        criar_usuário(c_usuario)
    elif resposta == "b":
        criar_conta_corrente(c_usuario, c_contas)
    elif resposta == "c":
        conta_selecionada = selecionar_conta(c_contas)
        if conta_selecionada:
            while True:
                resposta = Menu2(["[d] depositar", "[s] sacar", "[e] Extrato", "[q] Sair"])
                if resposta == "d":
                    cabeçalho("Depósito")
                    valor = leiaFloat("Insira um valor:")
                    conta_selecionada["saldo"] = realizar_deposito(
                        conta_selecionada["saldo"], valor, conta_selecionada["extrato"]
                    )
                elif resposta == "s":
                    cabeçalho("Saque")
                    saque = leiaFloat("Quanto você deseja sacar?")
                    conta_selecionada["saldo"], conta_selecionada["extrato"], conta_selecionada["numero_saques"] = realizar_saque(
                        saldo=conta_selecionada["saldo"],
                        valor=saque,
                        extrato=conta_selecionada["extrato"],
                        numero_saque=conta_selecionada["numero_saques"],
                        limite_saque=limite
                    )
                elif resposta == "e":
                    Extrato(conta_selecionada["saldo"], demonstrativo=conta_selecionada["extrato"])
                elif resposta == "q":
                    cabeçalho("O usuário decidiu sair...")
                    break
    elif resposta == "q":
        cabeçalho("O usuário decidiu sair...")
        break
    else:
        print("Opção Inválida")
