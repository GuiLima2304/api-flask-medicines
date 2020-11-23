#!/usr/bin/python3

import re
import sys
import mechanize
from xml.etree.ElementTree import XML, fromstring
import json
import os

from mechanize import Browser
from bs4 import BeautifulSoup
from urllib.request import urlopen


def GetFarmacologia(content):
    farmacologia.clear()
    pa_ini = content.find("Princípios Ativos")
    gf_ini = content.find("Grupos Farmacológicos")
    it_ini = content.find("Indicações Terapêuticas")
    it_fim = content.find("\n\n\n\n\nLaboratório")

    farmacologia["Principios Ativos"] = content[pa_ini + len("Princípios Ativos\n\n\n"):gf_ini-len("\n\n\n")]
    farmacologia["Grupos Farmacologicos"] = content[gf_ini + len("Grupos Farmacológicos\n\n\n"):it_ini-len("\n\n\n")]
    farmacologia["Indicacoes Terapeuticas"] = content[it_ini + len("Indicações Terapêuticas\n\n\n"):it_fim]


site = 'https://bulas.medicamentos.app/medicamentos'
bula = {}
farmacologia = {}
interacoesIsolada = ''

def GetBula(drug):
    medicamento = drug

    br = Browser()
    br.set_handle_robots(False)

    br.open(site)

    br.form = list(br.forms())[0]

    br['termo'] = medicamento

    page = br.submit()
    page = page.read()


    soup = BeautifulSoup(page, 'html.parser')
    tagsA = soup.find_all('a')

    title = 'title="' + medicamento.lower().capitalize() + '"'
    indices = [i for i, s in enumerate(tagsA) if title in str(s)]

    bula_url = tagsA[indices[0]]['href']

    page = urlopen(bula_url)
    page = page.read()

    soup = BeautifulSoup(page, 'html.parser')

    tagsH4 = soup.findAll('h4')
    topicos = list(map(lambda s: re.sub('</?h4>', '', str(s)), tagsH4))

    content = soup.getText()

    GetFarmacologia(content)

    for i in range(len(topicos) - 1):
        ini = content.find(topicos[i])
        fim = content.find(topicos[i + 1])
        bula[topicos[i]] = content[ini + len(topicos[i]):fim]

    bula[topicos[-1]] = content[fim+len(topicos[-1]):]
    bula[topicos[-1]] = re.sub('Gostaria de ter todas as.*', '', repr(bula[topicos[-1]]))
    bula[topicos[-1]] = re.sub('\\\\n', '\\n', bula[topicos[-1]])
    bula[topicos[-1]] = re.sub('\\n\\n', '', bula[topicos[-1]])


    interacoes = bula[topicos[2]]
    interacoes_pos = interacoes.find("Interações medicamentosas")
    interacoes = interacoes[interacoes_pos + len("Interações medicamentosas\n"):]
    interacoes = interacoes.strip()

    bula[topicos[-1]] = content[fim + len(topicos[-1]):]
    bula[topicos[-1]] = re.sub('"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"Gostaria.*', '', bula[topicos[-1]])

    with open(medicamento+'.json', 'w') as fout:
        fout.write('{\n')
        fout.write('    "titulo" : "' + medicamento + '",\n')
        fout.write('    "Interações medicamentosas" : "' + interacoes.strip().replace("\n", "\\n") + '",\n')

        for topico in farmacologia:
            fout.write('    "' + topico + '" : "' + farmacologia[topico].strip().replace("\n", "\\n") + '",\n')

        for topico in bula:
            if topico.find("quantidade maior do que a indicada") != -1:
                fout.write('    "' + topico + '" : "' + bula[topico].strip().replace("\n", "\\n") + '"\n')
            else:
                fout.write('    "' + topico + '" : "' + bula[topico].strip().replace("\n", "\\n") + '",\n')

        fout.write('}')

    with open(medicamento + '.json', 'r') as reader:
        data = json.loads(reader.read())

    os.remove(medicamento + '.json')

    return data

