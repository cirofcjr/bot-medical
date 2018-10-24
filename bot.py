import requests


url = "http://127.0.0.1:8000/"

class Cliente:
	pk= ""
	nome = ""
	cpf = ""
	data_nascimento = ""
	telefone = ""


print("Bom dia!")
var = input("Digite um numero:\n1- Agende sua consulta:")

if var == '1':
	get_cliente = 'clientes/?cpf='
	# 888.888.123-84
	# print(""Digite o seu CPF":")
	cpf = input("Qual o CPF do beneficiario que deseja a consulta?")
	requisicao = requests.get(url + get_cliente+cpf)
	resultado = requisicao.json()

	if len(resultado) == 1:
		resultado = resultado[0]
		cliente = Cliente()
		# print(resultado)
		cliente.pk=resultado['id']
		cliente.nome=resultado['nome']
		cliente.cpf=resultado['cpf']
		cliente.data_nascimento=resultado['data_nascimento']
		cliente.data_nascimento=resultado['data_nascimento']
		cliente.telefone=resultado['telefone']
		data_nascimento = input("Confirme a sua data de data_nascimento:")
		if cliente.data_nascimento == data_nascimento:
			print('ok')
	else:
		convenios = requests.get(url + "convenios/")
		convenios = convenios.json()
		print("Qual o seu convenio? ")
		for convenio in convenios:
			print(str(convenio['id'])+"- " + convenio['nome'])
		selecionar_convenio = input("Digite o convenio:")
		selecionar_convenio = int(selecionar_convenio) - 1
		convenio_id =  convenios[selecionar_convenio]['id']
		nome = input("Digite seu nome:")
		data_nascimento = input("Digite sua data de nascimento")
		telefone = input("Digite o numero do seu telefone")
		cpf = input("Digite seu cpf")
		sexo = input("M ou F:")

		#converter data de nascimento
		dia =data_nascimento.split('/')[0]
		mes = data_nascimento.split('/')[1]
		ano = data_nascimento.split('/')[2]
		data_nascimento = ano + "-" + mes + "-" + dia
		
		data = {
			    "nome": nome,
			    "cpf": cpf,
			    "telefone": telefone,
			    "data_nascimento": data_nascimento,
			    "sexo": sexo,
			    "convenio": convenio_id
			}

		cliente = requests.post(url +"clientes/", data=data)
		# print(cliente.json())



	r = requests.get(url + "especialidades/")
	dicionario = r.json()
	print("Escolha a especialidade:")


	for i in range(len(dicionario)):
		print(str(i+1) + " " + dicionario[i]['nome'])

	digitada = input("Digite a especialidade:")
	esp_id = int(digitada) - 1
	print(dicionario[esp_id]['descricao'])


	print("Deseja ser atendido por essa especialidade?\n1 - Sim\n2 - Não")
	opcao = input("Digite a opcao: ")
	if opcao == '1':
		print("Digite a data de preferencia:")

		r = requests.get(url + "especialidade/7/datas/")
		horarios = r.json()
		var = 1
		datas = {}
		for item in horarios:
			if item['data'] not in datas.values():
				datas[var] = item['data']
				var += 1
		for key, value in datas.items():
			print(str(key) + " " + value)
		posicao = input("Digite a opção: ")

		data_escolhida = datas[int(posicao)]
		final = data_escolhida.split("/")
		entry = "%2F"
		data = final[0] + entry + final[1] + entry + final[2]
		filtro = url + "especialidade/7/datas/?data=" + data
		filtrada = requests.get(filtro)
		horarios_vagos = {}
		horarios = filtrada.json()
		h = 1
		medicos = {}
		for item in horarios:
			if item['turno__tempo__inicio'] not in horarios_vagos:
				horarios_vagos[h] = item['turno__tempo__inicio']
				h += 1

		# print(horarios_vagos)
		for item in filtrada.json():
			if item['turno__tempo__inicio'] not in medicos:
				medicos[item['turno__tempo__inicio']] = {item["medico__pk"]:item['medico__nome']}
			else:
				medicos[item['turno__tempo__inicio']].update({item['medico__pk']:item['medico__nome']})

		m2 = {}
		v = 1
		for item in medicos:
			m2[v] = {item:medicos[item]}
			v += 1
		print("Escolha o horario:")
		
		for item in m2.items():
			for g in item[1]:
				print(str(item[0]) +"- "+ g)
		horario = input("Digite o horario: ")
		# print(m2[int(horario)])
		for key, value in m2[int(horario)].items():
			# print(key)
			horario_selecionado = key
		medicos_disponiveis = m2[int(horario)]
		var = ""
		for m in medicos_disponiveis:
			var = m
		medicos_para_o_horario = m2[int(horario)][var]
		# print(medicos_para_o_horario)
		indice = 1
		new_dicionario = {}
		for key, value in medicos_para_o_horario.items():
			new_dicionario[indice] = {'pk':key,'nome':value}
			indice += 1

		# print(new_dicionario)
		for key, value in new_dicionario.items():
			print(str(key)+"- " + value['nome'])
		medico_selecionado = input("Selecione o medico: ")
		id_medico_selecionado = new_dicionario[int(medico_selecionado)]['pk']
	
		dia = data_escolhida.split("/")[0]
		mes = data_escolhida.split("/")[1]
		ano = data_escolhida.split("/")[2]
		data_escolhida = ano+"-" +mes+"-"+dia

		data = {
		    "medico": id_medico_selecionado,
		    "cliente": cliente.pk,
		    "data": data_escolhida,
		    "inicio": horario_selecionado
		}
		criar_consulta = requests.post(url + "consultas/", data=data)
		print(criar_consulta.json())
		