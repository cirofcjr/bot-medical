import re
import datetime

year_atual = datetime.date.today().year.__str__()

# DD-MM-AAAA

# var = input("Digite")


def prefixo_ano(ano):
    year = year_atual[2:4]
    if ano > int(year):
        prefixo = '19'
        return prefixo + str(ano)
    else:
        prefixo = '20'
        return prefixo + str(ano)

# DD-MM-AAAA


def formato1(string):
    regex = re.findall(r"[0-3]\d-[0-1]\d-[1-2]\d{3}", string)
    if len(regex) != 0:
        return regex[0]
    else:
        return False


# DD/MM/AA
def formato2(string):
    regex = re.findall(r"[0-3]\d/[0-1]\d/\d{2}$", string)

    if len(regex) != 0:
        dia = regex[0].split("/")[0]
        mes = regex[0].split("/")[1]
        ano = regex[0].split("/")[2]
        ano = int(ano)
        year = year_atual[2:4]
        ano = prefixo_ano(ano)
        data = dia + '/' + mes + '/' + ano
        return data
    else:
        return False

# DD-MM-AA


def formato3(string):
    regex = re.findall(r"[0-3]\d-[0-1]\d-\d{2}", string)

    if len(regex) != 0:
        dia = regex[0].split("-")[0]
        mes = regex[0].split("-")[1]
        ano = regex[0].split("-")[2]
        ano = int(ano)
        year = year_atual[2:4]
        ano = prefixo_ano(ano)
        data = dia + '/' + mes + '/' + ano
        return data
    else:
        return False

# DD/MM/AAAA


def formato4(string):
    regex = re.findall(r"[0-3]\d/[0-1]\d/\d{4}$", string)

    if len(regex) != 0:
        return regex[0]
    else:
        return False


def valida_data(data):
    if formato1(data) != False:
        return formato1(data)
    if formato2(data) != False:
        return formato2(data)
    if formato3(data) != False:
        return formato3(data)
    if formato4(data) != False:
        return formato4(data)
    else:
        return False

# print(valida_data(var))
#([0-9]{3}\.?[0-9]{3}\.?[0-9]{3}\-?[0-9]{2}|)  xxx.xxx.xxx-xx


def cpf1(string):
    regex = re.findall(r"([0-9]{3}.[0-9]{3}.[0-9]{3}-[0-9]{2})", string)
    if len(regex) != 0:
        cpf = regex[0]
        p1 = cpf[0:3]
        p2 = cpf[4:7]
        p3 = cpf[8:11]
        p4 = cpf[12:]
        ponto = "."
        return p1 + ponto + p2 + ponto + p3 + "-" + p4
    else:
        return False


#([0-9]{3}?[0-9]{3}?[0-9]{3}\-?[0-9]{2}|) xxxxxxxxx-xx
def cpf2(string):
    regex = re.findall(r"[0-9]{3}[0-9]{3}[0-9]{3}\-[0-9]{2}", string)
    if len(regex) != 0:
        cpf = regex[0]
        p1 = cpf[0:3]
        p2 = cpf[3:6]
        p3 = cpf[6:9]
        p4 = cpf[10:]
        ponto = "."
        return p1 + ponto + p2 + ponto + p3 + "-" + p4
    else:
        return False


# ([0-9]{3}?[0-9]{3}?[0-9]{3}[0-9]{2}|) xxxxxxxxxxx
def cpf3(string):
    regex = re.findall(r"([0-9]{3}?[0-9]{3}?[0-9]{3}[0-9]{2})", string)
    if len(regex) != 0:

        cpf = regex[0]
        p1 = cpf[0:3]
        p2 = cpf[3:6]
        p3 = cpf[6:9]
        p4 = cpf[9:]
        ponto = "."
        return p1 + ponto + p2 + ponto + p3 + "-" + p4
    else:
        return False


def validacao_do_cpf(cpf):
    if cpf1(cpf) != False:
        return cpf1(cpf)
    if cpf2(cpf) != False:
        return cpf2(cpf)
    if cpf3(cpf) != False:
        return cpf3(cpf)
    else:
        return False
