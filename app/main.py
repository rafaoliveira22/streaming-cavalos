# TODO: Caso usuário já exista, mostra um menu com opções de filmes para assistir
# TODO: Criar opção de logout

import re
import requests
import sqlite3
import collections

print('Seja Bem Vindo ao Streaming Cavalos!\n1 - SignIn\n2 - SignUp')

#  REQUISIÇÃO VIA GET PARA A API VIA CEP,RETORNANDO O ENDEREÇO ENCONTRADO COM O CEP DIGITADO
def getRequestCEP(inputCEP):
    BASE_URL = requests.get(f'https://viacep.com.br/ws/{inputCEP}/json/')
    DATA_JSON = BASE_URL.json()

    return DATA_JSON

# LOGIN DO USUÁRIO
def login():
    statusLogin = ''
    while True:
        # usuário vai realizar o login
        userLogin = input('User: ')
        userPass = input('Senha: ')

        con = sqlite3.connect('teste3.db')
        cur = con.cursor()
        cur.execute(f"SELECT password FROM users where userName = '{userLogin}' ")
        found = cur.fetchall()
        if userPass == found[0][0]:
            statusLogin = 'logado'
            break
        else:
            statusLogin = 'login inválido'

        return statusLogin

# CADASTRO DE USUÁRIO
def register():
    print('Parece que você ainda nao tem um cadastro, vamo lá!')
    statusRegister = 'NOT OK'

    while True:
        if statusRegister == 'OK':
            break

        name = input('Primeiro nome: ')
        midName = input('Sobrenome: ')

        age = input('Idade: ')

        while True:
            cpf = input('CPF: ')
            if re.search(r'[a-z]', cpf, flags=re.I):
                print('Você digitou letras. CPF só aceita números')
            elif len(cpf) != 11:
                print('Você digitou números a mais ou a menos. Digite somente números: ')
            else: break

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
            database('teste3.db', user, command)
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
    print('dados inseridos no banco')

# RODA O PROGRAMA COMPLETO
def allOperations():
    while True:
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


