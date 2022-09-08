# TODO: Loja de streaming tipo, NETFLIX, HBO etc.
# TODO: Quando o usuário acessar o programa deverá haver opção de cadastro e de acesso, login, logon
# TODO: Coletar dados de cadastro de usuários (caso não haja)
# TODO: Coletar nome completo, separar para as varáveis: nome, sobrenome
# TODO: Coletar idade
# TODO: Coletar CPF: ATENÇÃO, não coloque seus dados originais
# TODO: Na coleta do CPF, deverá ser aceito somente números: 1203120398
# TODO: Coletar CEP, e apartir do cep preencher o restante dos dados, rua e cidade
# TODO: Perguntar se dados do CEP estão corretos
# TODO: Coletar número da casa
# TODO: Caso usuário já exista, mostra um menu com opções de filmes para assistir
# TODO: Criar opção de logout

import re
import requests
import sqlite3
import collections

print('Seja Bem Vindo ao Streaming Cavalos!\n1 - SignIn\n2 - SignUp')
def register():
    print('Parece que você ainda nao tem um cadastro, vamo lá!')
    statusRegister = 'NOT OK'

    while True:
        if statusRegister == 'OK':
            break

        name = input('Primeiro nome: ')
        midName = input('Sobrenome: ')
        age = input('Idade: ')
        cpf = input('CPF: ')
        cep = input('CEP: ')

        # verificar se os campos estão vazios
        if name == '' or midName == '' or age == '' or cpf == '' or cep == '':
            print('Algum dos campos estão vazios')
        else:

            user = {
                'name': name,
                'midName': midName,
                'age': age,
                'cpf': cpf,
                'cep': cep
            }
            # or
            # userTestCollection = collections.defaultdict(str)
            # userTestCollection['name'] = name
            # userTestCollection['midName'] = midName
            # userTestCollection['age'] = age
            # userTestCollection['cpf'] = cpf
            # userTestCollection['cep'] = cep

            print('Dados cadastrados com sucesso!')
            statusRegister = 'OK'

    return user

def login():
    statusLogin = 'NOT OK'
    while True:
        # usuário vai realizar o login
        userLogin = input('User: ')
        userPass = input('Senha: ')

        if userLogin == register()['userLogin'] and userPass == register()['userPass']:
            statusLogin = 'OK'
            break #PAREI AQUI - 07/09 - 23:13

def database(db, user, command):
    con = sqlite3.connect(db)
    cur = con.cursor()

    try:
        cur.execute('CREATE TABLE users (name, midName, age, cpf, cep)')
    except Exception as e:
        print('Erro na criação da tabela -> ', e.args)

    cur.execute(command)
    # "INSERT INTO users VALUES ('?,?,?,?,?')", ((user['name']),(user['midName']),(user['age']),(user['cpf']), (user['cep']))

def initialOption():
    while True:
        opLoginOrRegister = input('Opção: ')
        if re.search(r'[03-9a-zA-z]', opLoginOrRegister):
            print('Digite uma opção válida...1 ou 2')

        if opLoginOrRegister == '1':
            login()
            break
        elif opLoginOrRegister == '2':
            register()