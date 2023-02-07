import pandas as pd
from bs4 import BeautifulSoup as bs
import urllib.request
import requests
import lxml.html
from pymongo import MongoClient
from datetime import datetime
import re
import csv


def getSearchContent():
    payload = {
        "type": "ps",
        "ps_profession": "34",
        "ps_profession_label": "Médecin généraliste",
        "ps_localisation": "HERAULT(34)",
        "localisation_category": "departements",
    }

    url = "http://annuairesante.ameli.fr/recherche.html"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }
    session = requests.Session()
    page = session.post(url, params=payload, headers=header)

    return page


def get_fisrt_page_datas():
    page = getSearchContent()
    soup = bs(page.text, "html.parser")
    elements = soup.findAll("div", 'item-professionnel-inner')
    infos = []
    with open('students.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(["Name", "Number", "Adresse"])
        for n in range(len(elements)):

            name = (elements[n].find(class_="ignore-css").a.text)
            tel = ''
            try:
                tel = (elements[n].find(class_="tel").get_text())
            except:
                tel = ''

            adresse = (elements[n].find(class_="adresse").get_text())
            info = {
                "name": name,
                "number": tel.replace("\xa0", ""),
                'adresse': adresse
            }
            infos.append(info)
        for n in range(len(infos)):
            writer.writerow([infos[n]["name"], infos[n]["number"], infos[n]["adresse"]])

get_fisrt_page_datas()
