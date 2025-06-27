import requests
from flask import Flask, jsonify, request
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_estados():
    main_url = "https://www.portalbsd.com.br/"
    url = "https://www.portalbsd.com.br/tvterrestre.php"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    div_estados = soup.select_one("div.col-md-7.col-sm-7.col-xs-12")

    estados = []
    
    for a in div_estados.find_all("a", href=True):
        nome_estado = a.text.strip()
        link_estado = (main_url + a['href'])
        estados.append({"nome": nome_estado, "link": link_estado})

    return estados


def get_cidades(link_estado):
    estado = input("Digite a sigla do estado (ex: AC, SP, RJ): ").strip().upper()
    url = f"https://www.portalbsd.com.br/terrestres_cidades.php?estado={estado}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    tabela = soup.find("table")

    cidades = []
    tabelas = soup.find_all("table")
    if len(tabelas) > 1:
        tabela = tabelas[1]
    else:
        tabela = None

    if not tabela:
        print(f"Nenhuma tabela encontrada para o estado {estado}")
        return []

    for a in tabela.find_all("a", href=True):
        nome_cidade = a.text.strip()
        link_completo = "https://www.portalbsd.com.br/" + a["href"]
        cidades.append({
            "nome": nome_cidade,
            "link": link_completo
        })

    return cidades
    print (cidades)

if __name__ == "__main__":
    cidades = get_cidades(link_estado=None)
    for cidade in cidades:
        print(f"{cidade['nome']}: {cidade['link']}")

