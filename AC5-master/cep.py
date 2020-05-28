import requests

cep_input = input('Digite o CEP para a consulta: ')

if len(cep_input) != 8:
    print("Quantidade de digitos invalida!")
    exit()

request = requests.get('https://viacep.com.br/ws/{}/json/'.format(cep_input))
address_data = request.json()

if 'erro' not in address_data:
    print(request.json())
else:
    print('CEP invalido.')