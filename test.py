#!/usr/bin/python3

import re
import sys
import mechanize
from xml.etree.ElementTree import XML, fromstring
import json

from mechanize import Browser
from bs4 import BeautifulSoup
from urllib.request import urlopen


def printTopicos(topicos):
    for t in topicos:
        print(t)


def printTextos(topico):

    bulas = ''   
    cont = 0

    topicoEspecial = {}
    topicoEspecial['teste'] = []

    for ch in bula:
        bulas += bula[ch]

        if(ch):            
            topicoEspecial['teste'].append(
                {
                    'title':ch, 
                    'description':bula[ch]
                }
            )
            print('\n\n')
            print(topicoEspecial)
            print('\n\n')
            cont += 1

    return topicoEspecial

       
# def printTextos(topico):
#     for ch in bula:
#         if(ch == 'Interações medicamentosas'):
#             print(ch + '\n#' + bula[ch] + '\n\n')
#             return bula[ch]

site = 'https://bulas.medicamentos.app/medicamentos'
# medicamento = ''
bula = {}

def startMedicamentos(drug1):
    medicamento = drug1
    print(medicamento)


def teste(drug1):
    medicamento = drug1

    br = Browser()
    br.set_handle_robots(False)

    br.open(site)

    br.form = list(br.forms())[0]

    br['termo'] = medicamento
    print(medicamento)

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

    # tagsStrong = soup.findAll('strong')
    # topicos = list(map(lambda s: re.sub('</?strong>', '', str(s)), tagsStrong))



    content = soup.getText()

    for i in range(len(topicos) - 1):
        ini = content.find(topicos[i])
        fim = content.find(topicos[i + 1])
        bula[topicos[i]] = content[ini + len(topicos[i]):fim]

    bula[topicos[-1]] = content[fim + len(topicos[-1]):]

    resultado  = printTextos(bula)

    return resultado



# printTopicos(topicos)
# print('\n\n')
# printTextos(bula)
