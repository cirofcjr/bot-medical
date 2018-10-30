import telepot
import requests

url = "http://127.0.0.1:8000/"


class Cliente:
    pk = ""
    nome = ""
    cpf = ""
    data_nascimento = ""
    telefone = ""


class Especialidade:
    pk = ""
    nome = ""
    descricao = ""


class Bot():

    # cliente = Cliente()

    mensagens_enviadas = []
    cliente = ""
    especialidade = ""
    dicionario = {}
    m2 = {}
    horarios = {}

    def inicio_conversa(msg=None):
        # print(mensagem)
        boa_tarde = "Boa Tarde!"
        # self.mensagens_enviadas.append(boa_tarde)
        # print(self.mensagens_enviadas)
        mensagem = "Digite a opção desejada:\n 1 - Você deseja agendar consulta"

        return boa_tarde + '\n' + mensagem

    def pedir_cpf(self, number=None):
        if number == "1":
            msg1 = "Digite seu CPF: "
            return msg1

    def validar_nascimento(self, msg, data_nascimento):
        if msg == data_nascimento:
            return self.list_especialidades()
        else:
            return False

    def valida_cpf(self, cpf=""):
        get_cliente = 'clientes/?cpf='
        requisicao = requests.get(url + get_cliente + cpf)
        resultado = requisicao.json()
        if len(resultado) == 1:
            resultado = resultado[0]
            cliente = Cliente()
            # print(resultado)
            cliente.pk = resultado['id']
            cliente.nome = resultado['nome']
            cliente.cpf = resultado['cpf']
            cliente.data_nascimento = resultado['data_nascimento']
            cliente.data_nascimento = resultado['data_nascimento']
            cliente.telefone = resultado['telefone']
            return cliente
            # data_nascimento = input(
            #     "Confirme a sua data de data_nascimento:")
            # if cliente.data_nascimento == data_nascimento:
            #     print('ok')
            # return cliente

    def criar_especialidade(self, id):
        r = requests.get(url + "especialidades/")
        pk = r.json()[int(id) - 1]['id']
        req = requests.get(url + 'especialidade/' + str(pk))
        especialidade = Especialidade()
        json = req.json()
        especialidade.id = json['id']
        especialidade.nome = json['nome']
        especialidade.descricao = json['descricao']
        self.dict('especialidade', especialidade.id)
        return especialidade

    def list_especialidades(self):
        r = requests.get(url + "especialidades/")
        dicionario = r.json()
        mensagem = "Você deseja ser atendido por qual especialidade? \n"

        for i in range(len(dicionario)):
            mensagem += str(i + 1) + " " + dicionario[i]['nome'] + '\n'
        return mensagem

    def datas_disponiveis_para_especialidade(self):
        especialidade_id = self.dicionario['especialidade']
        r = requests.get(url + "especialidade/" + especialidade_id + "/datas/")
        horarios = r.json()
        var = 1
        datas = {}
        mensagem = "Escolha a data: \n"
        for item in horarios:
            if item['data'] not in datas.values():
                datas[var] = item['data']
                var += 1
        for key, value in datas.items():
            mensagem += str(key) + "-  " + value + '\n'
        return mensagem

    def data_escolhida(self, id):
        especialidade_id = self.dicionario['especialidade']

        r = requests.get(url + "especialidade/" + especialidade_id + "/datas/")
        horarios = r.json()
        var = 1
        datas = {}
        for item in horarios:
            if item['data'] not in datas.values():
                datas[var] = item['data']
                var += 1
        data_escolhida = datas[int(id)]
        dia = data_escolhida.split("/")[0]
        mes = data_escolhida.split("/")[1]
        ano = data_escolhida.split("/")[2]
        dta = ano + "-" + mes + "-" + dia
        self.dicionario['data'] = dta

        final = data_escolhida.split("/")
        entry = "%2F"
        data = final[0] + entry + final[1] + entry + final[2]
        filtro = url + "especialidade/"+especialidade_id+"/datas/?data=" + data
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
                medicos[item['turno__tempo__inicio']] = {
                    item["medico__pk"]: item['medico__nome']}
            else:
                medicos[item['turno__tempo__inicio']].update(
                    {item['medico__pk']: item['medico__nome']})

        m2 = {}
        v = 1
        for item in medicos:
            m2[v] = {item: medicos[item]}
            v += 1
        mensagem = "Escolha o horario: \n"
        self.m2 = m2
        for item in m2.items():
            for g in item[1]:
                self.horarios[item[0]] = g
                mensagem += str(item[0]) + "- " + g + '\n'
        return mensagem

    def dict(self, string, test):
        self.dicionario[string] = str(test)

    def seleciona_medico(self, id):
        hour = self.horarios[int(id)]
        print(hour)
        horario = id
        self.dict('horario', hour)
        m2 = self.m2
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
            new_dicionario[indice] = {'pk': key, 'nome': value}
            indice += 1

        # print(new_dicionario)
        mensagem = ""
        for key, value in new_dicionario.items():
            mensagem += str(key) + "- " + value['nome'] + '\n'
        return mensagem
    def get_medico_selecionado(self, id):
        hour = self.horarios[int(id)]
        horario = id
        m2 = self.m2
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
            new_dicionario[indice] = {'pk': key, 'nome': value}
            indice += 1
        return  new_dicionario

    def post_consulta(self):
        dicionario = self.dicionario
        data = {
            "medico": dicionario['medico'],
            "cliente": dicionario['cliente'],
            "data": dicionario['data'],
            "inicio": dicionario['horario']
        }
        criar_consulta = requests.post(url + "consultas/", data=data)
        if criar_consulta.status_code == 201:
            return "Agendado com sucesso!!!"
        else:
            return "Error!!!"


    def pensa(self, msg=None):

        self.mensagens_enviadas.append(msg)
        if len(self.mensagens_enviadas) == 1:
            return self.inicio_conversa()
        if len(self.mensagens_enviadas) == 2:
            # print(msg)
            return self.pedir_cpf(msg)
        if len(self.mensagens_enviadas) == 3:
            self.cliente = self.valida_cpf(msg)
            self.dict('cliente', self.cliente.pk)
            return "Confirme sua data de nascimento:"
        if len(self.mensagens_enviadas) == 4:
            return self.validar_nascimento(msg, self.cliente.data_nascimento)
            # True:

        if len(self.mensagens_enviadas) == 5:
            self.especialidade = self.criar_especialidade(msg)
            return self.especialidade.descricao + '\n' + "Deseja ser atendido por essa especialidade ?\n1 - Sim\n2 - Não "
        if len(self.mensagens_enviadas) == 6:
            return self.datas_disponiveis_para_especialidade()
        if len(self.mensagens_enviadas) == 7:
            return self.data_escolhida(msg)
        if len(self.mensagens_enviadas) == 8:
            return self.seleciona_medico(msg)
        if len(self.mensagens_enviadas) == 9:
            pk_medico = self.get_medico_selecionado(msg)[int(msg)]['pk']
            self.dicionario['medico'] = pk_medico
            print(self.dicionario)
            return self.post_consulta()

            # return self.datas_disponiveis_para_especialidade(msg,
            # self.especialidade.pk)

            # def enviar_mensagem(self, msg=None):
            #     if len(self.mensagens_enviadas) == 0:

            # if len(self.mensagens_enviadas) == 1:
            #     if msg == '1':

            #         self.mensagens_enviadas.append("ok")
            #         r = requests.get("http://127.0.0.1:8000/especialidades/")

            #         lista = r.json()
            #         string = "Qual a especialidade que você deseja realizar a consulta:\n "
            #         for i in range(len(lista)):
            #             string += str(i + 1) + " - " + lista[i]['nome'] + '\n'
            #         return string
            #     else:
            #         mensagem = "Digite a opção desejada:\n 1 - Você deseja agendar consulta"

            # return "Desculpa não entendi, por favor digite a opção
            # novamente\n" + mensagem

    def get_cliente(self, number="", cpf=""):
        get_cliente = 'clientes/?cpf='
        if number == 1:
            print("passou")
        # 888.888.123-84
        # print(""Digite o seu CPF":")
        # cpf = input("Qual o CPF do beneficiario que deseja a consulta?")
        # requisicao = requests.get(url + get_cliente + cpf)
        # resultado = requisicao.json()
        # if len(resultado) == 1:
        #     resultado = resultado[0]
        #     cliente = Cliente()
        #     # print(resultado)
        #     cliente.pk = resultado['id']
        #     cliente.nome = resultado['nome']
        #     cliente.cpf = resultado['cpf']
        #     cliente.data_nascimento = resultado['data_nascimento']
        #     cliente.data_nascimento = resultado['data_nascimento']
        #     cliente.telefone = resultado['telefone']
        #     data_nascimento = input(
        #         "Confirme a sua data de data_nascimento:")
        #     if cliente.data_nascimento == data_nascimento:
        #         print('ok')
        #     return cliente


telegram = telepot.Bot("771366635:AAGWjSGgYTyICMq9vC1lMa5yTQt_1YzE2XY")

bot = Bot()


def receber_msg(msg):
    mensagem = bot.pensa(msg['text'])
    id = msg['chat']['id']
    telegram.sendMessage(id, mensagem)

    # print(mensagem)

telegram.message_loop(receber_msg)


while True:
    pass
