
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
    new_cliente = Cliente()
    var = None
    cria_usuario = None
    mensagens_enviadas = {}
    especialidade = ""
    dicionario = {}
    m2 = {}
    contador = 0
    horarios = {}
    data_cliente = {
        "nome": "",
        "cpf": "",
        "telefone": "",
        "data_nascimento": None,
        "sexo": None,
        "convenio": None

    }

    def inicio_conversa(msg=None):
        boa_tarde = "Bom dia!"
        mensagem = "Digite a opção desejada:\n 1 - Você deseja agendar consulta"
        return boa_tarde + '\n' + mensagem

    def pedir_cpf(self, number=None):
        if number == "1":
            msg1 = "Precisamos do CPF do beneficiario que deseja o agendamento:"
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
            self.new_cliente.pk = resultado['id']
            self.new_cliente.nome = resultado['nome']
            self.new_cliente.cpf = resultado['cpf']
            self.new_cliente.data_nascimento = resultado['data_nascimento']
            self.new_cliente.data_nascimento = resultado['data_nascimento']
            self.new_cliente.telefone = resultado['telefone']
            return self.new_cliente
        else:
            return False

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
        filtro = url + "especialidade/" + especialidade_id + "/datas/?data=" + data
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
        horario = id
        self.dict('horario', hour)
        m2 = self.m2
        for key, value in m2[int(horario)].items():
            horario_selecionado = key
        medicos_disponiveis = m2[int(horario)]
        var = ""
        for m in medicos_disponiveis:
            var = m
        medicos_para_o_horario = m2[int(horario)][var]
        indice = 1
        new_dicionario = {}
        for key, value in medicos_para_o_horario.items():
            new_dicionario[indice] = {'pk': key, 'nome': value}
            indice += 1

        mensagem = "Selecione o medico:\n"
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
        indice = 1
        new_dicionario = {}
        for key, value in medicos_para_o_horario.items():
            new_dicionario[indice] = {'pk': key, 'nome': value}
            indice += 1
        return new_dicionario

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

    def criar_cliente(self, msg):
        convenios = requests.get(url + 'convenios/')
        convenio_selecionado = ""

        cliente = self.new_cliente
        data = self.data_cliente
        if cliente.nome == "":
            self.new_cliente.nome = msg
            data['nome'] = cliente.nome
            return "Confirme o CPF do cliente:"
        if cliente.cpf == "":
            cliente.cpf = msg
            data['cpf'] = cliente.cpf
            return "Informe a sua data de nascimento:"
        if cliente.data_nascimento == "":
            dia = msg.split("/")[0]
            mes = msg.split("/")[1]
            ano = msg.split("/")[2]
            dta = ano + "-" + mes + "-" + dia
            cliente.data_nascimento = msg
            data['data_nascimento'] = dta
            return "Digite o numero do seu telefone com DDD"
        if cliente.telefone == "":
            cliente.telefone = msg
            data['telefone'] = cliente.telefone
            count = 0
            list_convenios = convenios.json()
            var = "Qual o seu convenio?\n"
            for convenio in list_convenios:
                var += str(count + 1) + ' - ' + convenio['nome'] + '\n'
                count += 1
            return var
        if data['convenio'] == None:
            list_convenios = convenios.json()
            selecionado = ""
            count = 0
            dicionario = {}
            for convenio in list_convenios:
                dicionario[str(count + 1)] = convenio['nome']
                count += 1

            for convenio in list_convenios:
                if convenio['nome'] == dicionario[msg]:
                    convenio_selecionado = convenio['id']
            data["convenio"] = convenio_selecionado
            return "Qual o sexo do cliente\n" + "1 - Masculino\n" + "2 - Feminino"
        if data['sexo'] == None:
            print(msg)
            if msg == "1":
                data['sexo'] = "M"
            if msg == "2":
                data['sexo'] = "F"
            post_cliente = requests.post(
                url + "clientes/", data=self.data_cliente)
            if post_cliente.status_code == 201:
                self.var = True
                self.dict('cliente', post_cliente.json()['id'])
                return cliente.nome + " \n" + cliente.data_nascimento + " \n" + cliente.telefone + "\n" + "Os dados estão corretos?\n 1- Sim\n 2- Não "

    def pensa(self, msg=None, chat_id=None):

        self.contador += 1
        if chat_id not in self.mensagens_enviadas:
            self.mensagens_enviadas[chat_id] = {}
        self.mensagens_enviadas[chat_id][self.contador] = msg
        if len(self.mensagens_enviadas[chat_id]) == 1:
            return self.inicio_conversa()
        if len(self.mensagens_enviadas[chat_id]) == 2:
            return self.pedir_cpf(msg)
        if len(self.mensagens_enviadas[chat_id]) == 3:
            if self.var == None:
                if self.valida_cpf(msg) != False:
                    self.dict('cliente', self.new_cliente.pk)
                    return "Oi, " + self.new_cliente.nome + "\nConfirme sua data de nascimento:"
                else:
                    self.var = False
            if self.var == False:
                self.mensagens_enviadas[chat_id].pop(self.contador)
                if self.cria_usuario == None:
                    self.cria_usuario = True
                    return "Informe o nome do cliente:"

                return self.criar_cliente(msg)
            if self.var == True:
                self.mensagens_enviadas[chat_id][self.contador] = msg
                return "Confirme a data de nascimento:"

        if len(self.mensagens_enviadas[chat_id]) == 4:
            if self.validar_nascimento(msg, self.new_cliente.data_nascimento) != False:
                return self.validar_nascimento(msg, self.new_cliente.data_nascimento)
            else:
                self.mensagens_enviadas[chat_id].pop(self.contador)
                return "A data de nascimento informada:" + msg + " não consta em nosso sistema você pode tentar novamente digitar a data correta:"

        if len(self.mensagens_enviadas[chat_id]) == 5:
            self.especialidade = self.criar_especialidade(msg)
            return self.especialidade.descricao + '\n' + "Deseja ser atendido por essa especialidade ?\n1 - Sim\n2 - Não "
        if len(self.mensagens_enviadas[chat_id]) == 6:
            return self.datas_disponiveis_para_especialidade()
        if len(self.mensagens_enviadas[chat_id]) == 7:
            return self.data_escolhida(msg)
        if len(self.mensagens_enviadas[chat_id]) == 8:
            return self.seleciona_medico(msg)
        if len(self.mensagens_enviadas[chat_id]) == 9:
            pk_medico = self.get_medico_selecionado(msg)[int(msg)]['pk']
            self.dicionario['medico'] = pk_medico
            print(self.dicionario)
            return self.post_consulta()

    def get_cliente(self, number="", cpf=""):
        get_cliente = 'clientes/?cpf='
        if number == 1:
            print("passou")


telegram = telepot.Bot("771366635:AAGWjSGgYTyICMq9vC1lMa5yTQt_1YzE2XY")

bot = Bot()


def receber_msg(msg):
    id = msg['chat']['id']

    mensagem = bot.pensa(msg['text'], chat_id=id)
    telegram.sendMessage(id, mensagem)

    # print(mensagem)

telegram.message_loop(receber_msg)

while True:
    pass
