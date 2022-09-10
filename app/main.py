import re
import requests
import sqlite3

#  REQUISIÇÃO VIA GET PARA A API VIA CEP,RETORNANDO O ENDEREÇO ENCONTRADO COM O CEP DIGITADO
def getRequestCEP(inputCEP):
    BASE_URL = requests.get(f'https://viacep.com.br/ws/{inputCEP}/json/')
    DATA_JSON = BASE_URL.json()

    return DATA_JSON

#  REQUISIÇÃO VIA GET PARA A API VIA CEP,RETORNANDO O ENDEREÇO ENCONTRADO COM O CEP DIGITADO
def getRequestMovies():
    key = '' # sua key da API MoviesDB
    BASE_URL = requests.get(f'https://api.themoviedb.org/3/movie/popular?api_key={key}&language=en-US&page=1')
    DATA_JSON = BASE_URL.json()

    return DATA_JSON['results']

# LOGIN DO USUÁRIO
def login():
    statusLogin = ''
    opNotLogin = ''
    while True:
        # usuário vai realizar o login
        print('\n<<< LOGIN >>>')
        userLogin = input('User: ')
        userPass = input('Senha: ')


        con = sqlite3.connect('streamingCavalos.db')
        cur = con.cursor()
        cur.execute(f"SELECT password FROM users where userName = '{userLogin}' ")
        found = cur.fetchall()

        if userPass == found[0][0]:
            statusLogin = 'Logado'
            print(statusLogin)
            listMovies()
            break
        else:
            statusLogin = 'Login inválido'
            opNotLogin = input(f'{statusLogin}. O que deseja fazer agora?\n1 - Cadastro\n2 - Login\nOpção: ')
            if opNotLogin == '1':
                register()
            elif opNotLogin == '2':
                login()

        return statusLogin


# CADASTRO DE USUÁRIO
def register():
    print('\n<<< CADASTRO >>>')
    print('Parece que você ainda nao tem um cadastro, vamo lá!')
    statusRegister = 'NOT OK'

    while True:
        if statusRegister == 'OK':
            break

        name = input('Primeiro nome: ')
        midName = input('Sobrenome: ')

        age = input('Idade: ')

        cpf = input('CPF: ')
        if re.search(r'[a-z]', cpf, flags=re.I):
            print('Você digitou letras. CEP só aceita números')
        elif len(cpf) != 11:
            print('Você digitou números a mais ou a menos. Digite somente números: ')

        while True:
            cep = input('CEP: ')
            if re.search(r'[a-z]', cep, flags=re.I):
                print('Você digitou letras. CEP só aceita números')
            elif len(cep) != 8:
                print('Você digitou números a mais ou a menos. Digite somente números: ')
            else:
                print(
                    f'O seu CEP é: {cep}. Os dados abaixo estão corretos:\nCidade: {getRequestCEP(cep)["localidade"]}\nBairro: {getRequestCEP(cep)["bairro"]}\nRua: {getRequestCEP(cep)["logradouro"]}')
                statusCEP = input('1- Sim. CEP Correto\n2 - Não. CEP Incorreto\nOpção: ')
                if statusCEP == '1':
                    numberHouse = input('Número da casa: ')
                    break
                elif statusCEP == '2':
                    print('OK. Vamos lá denovo...')


        userName = input('Nome de usuário para login: ')
        password = input('Senha para login: ')

        # verificar se os campos estão vazios
        if name == '' or midName == '' or age == '' or cpf == '' or cep == '':
            print('Algum dos campos estão vazios. Preencha todos os campos e tente novamente')
        else:
            user = {
                'name': name,
                'midName': midName,
                'age': age,
                'cpf': cpf,
                'cep': cep,
                'numberHouse': numberHouse,
                'userName': userName,
                'password': password
            }
            print('Dados cadastrados com sucesso! Vamos ao login...')

            # inserindo dados do registro no banco
            command = f'INSERT INTO users (name, midName, age, cpf, cep, numberHouse, userName, password) VALUES ("{user["name"]}", ' \
              f'"{user["midName"]}",' \
              f'"{user["age"]}", ' \
              f'"{user["cpf"]}", ' \
              f'"{user["cep"]}", ' \
              f'"{user["numberHouse"]}", ' \
              f'"{user["userName"]}", ' \
              f'"{user["password"]}");'
            database('streamingCavalos.db', user, command)
            statusRegister = 'OK'

        return user

# FUNÇÕES PARA O BANCO DE DADOS
def database(db, user, command):
    con = sqlite3.connect(db)
    cur = con.cursor()

    try:
        cur.execute('CREATE TABLE users (name, midName, age, cpf, cep, numberHouse, userName, password)')
    except Exception as e:
        # print('Erro na criação da tabela -> ', e.args)
        pass

    # cur.execute(command)
    con.execute(command)
    con.commit()
    con.close()

def listMovies():
    while True:
        i = 0

        print('\n<<< STREAMING CAVALOS >>>\nFilmes disponiveis: ')
        while True:
            if i >= 20:
                break
            else:
                #listar os filmes -> usuario vai escolher  -> 'filme rolando' -> sair do filme -> loop
                print(f'{i+1} - {getRequestMovies()[i]["original_title"]}')
                i = i + 1

        opMovie = input('\n0 - Deslogar\nOpção: ')
        if opMovie == '0':
                logout()
        elif int(opMovie) > 0 and int(opMovie) <= 20:
            while True:
                print('Boa escolha,rodando seu filme...')
                opStopMovie = input('\nPara sair digite 1: ')
                if opStopMovie == '1':
                    confirmStop = input('Deseja realmente sair do filme?\n1 - Sim\n2 - Não\nOpção: ')
                    if confirmStop == '1':
                        break
        else:
            print('Opção inválida...')


def logout():
    print('\n<<< LOGOUT >>>')
    statusLogout = input('\nDeseja realmente deslogar da sua conta?\n1 - Sim\n2 - Não. Continuar Navegando...\nOpção: ')
    if statusLogout == '1':
        print('Encerrando sessão...Até a próxima')
        allOperations()
    elif statusLogout == '2':
        listMovies()

    return statusLogout

# RODA O PROGRAMA COMPLETO
def allOperations():
    while True:
        print('Seja Bem Vindo ao Streaming Cavalos!\n1 - SignIn\n2 - SignUp')
        opLoginOrRegister = input('Opção: ')

        if opLoginOrRegister == '1':
            login()
            break
        elif opLoginOrRegister == '2':
            register()
            login()
            break
        else:
            print('Digite uma opção válida...1 ou 2')

allOperations()

# EM TESTE...
# def verifyCharacters(exp, length):
#     while True:
#         print(f'ta vindo isso: {exp}')
#         if re.search(r'[a-z]', exp, flags=re.I) or len(exp) != length:
#             print('Cadastro Incorreto. Lembre-se: Não digite letras nem caracteres a mais ou a menos...')
#             exp = input('Digite novamente: ')
#         else: break
#
#
#     return exp


