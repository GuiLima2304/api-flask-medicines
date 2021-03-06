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


def printTopicos(topicos):
    for t in topicos:
        print(t)

def printFarmacologia(content):
    farmacologia.clear()
    pa_ini = content.find("Princípios Ativos")
    gf_ini = content.find("Grupos Farmacológicos")
    it_ini = content.find("Indicações Terapêuticas")
    it_fim = content.find("\n\n\n\n\nLaboratório")

    farmacologia["Principios Ativos"] = content[pa_ini + len("Princípios Ativos\n\n\n"):gf_ini-len("\n\n\n")]
    farmacologia["Grupos Farmacologicos"] = content[gf_ini + len("Grupos Farmacológicos\n\n\n"):it_ini-len("\n\n\n")]
    farmacologia["Indicacoes Terapeuticas"] = content[it_ini + len("Indicações Terapêuticas\n\n\n"):it_fim]
    print('\n\n')
    print('----------------------------------------------------FARMACOLOGIA--------------------------------------------------')
    print(farmacologia)

def printInteracoes(interacoes):
    interacoes_pos = interacoes.find("Interações medicamentosas")
    interacoes = interacoes[interacoes_pos + len("Interações medicamentosas\n"):]
    interacoes = interacoes.strip()
    interacoesIsolada = interacoes
    print('INTERACOES ISOLADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
    print(interacoesIsolada)
    return interacoesIsolada

def printTextos(topico):

    bulas = ''   
    cont = 0

    topicoEspecial = {}
    topicoEspecial['bula'] = []

    print(farmacologia)

    for ch in bula:
        bulas += bula[ch]

        topicoEspecial['bula'].append(
            {
                'title':ch, 
                'description':bula[ch]
            },
        ),
        topicoEspecial['farmacologia'] = farmacologia,
    
    topicoEspecial['interacao'] = { 'teste':interacoesIsolada }


        # print('\n\n')
        # print(topicoEspecial)
        # print('\n\n')
        # cont += 1

    # topicoEspecial['farmaco'].append(
    #     {
    #         'farmaco':farmacologia
    #     }
    # )
    return topicoEspecial

       
# def printTextos(topico):
#     for ch in bula:
#         if(ch == 'Interações medicamentosas'):
#             print(ch + '\n#' + bula[ch] + '\n\n')
#             return bula[ch]

site = 'https://bulas.medicamentos.app/medicamentos'
# medicamento = ''
bula = {}
farmacologia = {}
interacoesIsolada = ''


def startMedicamentos(drug1):
    medicamento = drug1
    # print(medicamento)


def teste(drug1):
    medicamento = drug1

    br = Browser()
    br.set_handle_robots(False)

    br.open(site)

    br.form = list(br.forms())[0]

    br['termo'] = medicamento
    # print(medicamento)

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

    printFarmacologia(content)

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
    # printInteracoes(interacoes)
    interacoes = interacoes[interacoes_pos + len("Interações medicamentosas\n"):]
    interacoes = interacoes.strip()

    print('\n\n')
    print('----------------------------------------------------INTERACOES--------------------------------------------------')
    print(interacoes)
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
    print(data)

    # resultado  = printTextos(bula)

    return data



# printTopicos(topicos)
# print('\n\n')
# printTextos(bula)
