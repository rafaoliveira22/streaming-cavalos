# TODO: Caso usuário já exista, mostra um menu com opções de filmes para assistir
# TODO: Criar opção de logout

import re
import requests
import sqlite3
import collections

print('Seja Bem Vindo ao Streaming Cavalos!\n1 - SignIn\n2 - SignUp')

def getRequestCEP(inputCEP):
    BASE_URL = requests.get(f'https://viacep.com.br/ws/{inputCEP}/json/')
    DATA_JSON = BASE_URL.json()

    return DATA_JSON

def login():
    statusLogin = 'NOT OK'
    while True:
        # usuário vai realizar o login
        userLogin = input('User: ')
        userPass = input('Senha: ')
        break


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

# FUNÇÕES DE VERIFICAÇÃO
def verifyLettersInExpression(exp):
    while True:
        if re.search(r'[a-zA-z]', exp):
            print(f'Erro! Você utilizou letras: {exp}. Digite apenas números')
            exp = input('Digite novamente,mas somente números: ')
        else: break
    return exp

def verifyLength(exp,length):
    while True:
        if len(exp) != length:
            print(f'Você digitou caracters a mais ou a menos: {exp}. Digite apenas {length} corretamente')
            exp = input('Digite novamente,mas a quantidade correta de caracteres: ')
        else: break

    return exp
# FUNÇÕES PARA O BANCO DE DADOS
def database(db, user, command):
    con = sqlite3.connect(db)
    cur = con.cursor()

    try:
        cur.execute('CREATE TABLE users (name, midName, age, cpf, cep, numberHouse)')
    except Exception as e:
        # print('Erro na criação da tabela -> ', e.args)
        pass

    # cur.execute(command)
    con.execute(command)
    con.commit()
    con.close()
    print('dados inseridos no banco')

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

        # verificar se os campos estão vazios
        if name == '' or midName == '' or age == '' or cpf == '' or cep == '':
            print('Algum dos campos estão vazios. Preencha todos os campos e tente novamente')
        # se os campos nao estiverem vazios, verificar o tamanho do cpf,o máximo de caracteres é 11

        else:
            user = {
                'name': name,
                'midName': midName,
                'age': age,
                'cpf': cpf,
                'cep': cep,
                'numberHouse': numberHouse
            }
            print('Dados cadastrados com sucesso! Vamos ao login...')

            # inserindo dados do registro no banco
            command = f'INSERT INTO users (name, midName, age, cpf, cep, numberHouse) VALUES ("{user["name"]}", ' \
              f'"{user["midName"]}",' \
              f'"{user["age"]}", ' \
              f'"{user["cpf"]}", ' \
              f'"{user["cep"]}", ' \
              f'"{user["numberHouse"]}");'
            database('teste2.db', user, command)
            statusRegister = 'OK'

        return user
allOperations()


