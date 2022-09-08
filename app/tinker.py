



def register():
    name = input('Primeiro nome: ')
    midName = input('Sobrenome: ')
    age = input('Idade: ')
    cpf = input('CPF: ')
    cep = input('CEP: ')

    user = {
        'name': name,
        'midName': midName,
        'age': age,
        'cpf': cpf,
        'cep': cep
    }

    for i in user:
        print(user[i])

register()

