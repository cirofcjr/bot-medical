import requests 

url = ("http://127.0.0.1:8000/")


# create especialidade

# data = {"nome":"Ortopedista"}
# especialidade = requests.post(url + "especialidades/", data=data)
# print(especialidade.status_code, especialidade.reason, especialidade.json())

# create medico

especialidade = requests.get(url + "especialidade/7")
id_especialidade = especialidade.json()['id']
data = {"nome":"Jose", "crm":"323-PI","especialidade": id_especialidade}
medico = requests.post(url + "medicos/", data=data)
print(medico.status_code, medico.reason)

