
def getUrl(paginacao):
    return "https://mg.olx.com.br/belo-horizonte-e-regiao/autos-e-pecas/motos?o="+str(paginacao)+"&pe=11000&ps=2000&re=39&rs=18&sf=1"

def coletaLinks():
# Coleta os links das paginas de anuncios:
    from bs4 import BeautifulSoup
    import requests
    import re
    
    opt = int(input('Quantas páginas? '))
    links = []
    cont = 0
    for pag in range(1, opt + 1):
        print(f'- Lendo página {pag}...')
        URL = getUrl(pag)
        HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                    (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
                    'Accept-Language': 'en-US, en;q=0.5'})
        webpage = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(webpage.content, "html.parser")
        for link in soup.find_all('a', attrs={'href': re.compile("^https://")}):
            if '/motos/' in link.get('href'):
                cont += 1
                links.append(link.get('href'))
    
    print('='*100)
    print(f'------ {opt} páginas percorridas.')
    print(f'------ {len(links)} links encontrados.')
    return links

def exclui_links_existentes(lista_nova):
    import os.path
        
    if os.path.isfile('links_lst.json'):
        lista_armazenada = carrega_json('links_lst.json')
        print(f'------ Haviam {len(lista_armazenada)} links na lista armazenada.')
        
        linksDeAnunciosColetados = []
        anunciosColetados = carrega_json('dados_anuncios_capturados.json')
        for anuncio in anunciosColetados:
            linksDeAnunciosColetados.append(anuncio['Url'])
        
        cont_a = 0
        for link in lista_armazenada:
            if link not in linksDeAnunciosColetados:
                del lista_armazenada[cont_a]

        cont_apagados = 0
        cont = 0
        for link in lista_nova:
            if link in lista_armazenada:
                del lista_nova[cont]
                cont_apagados += 1
            cont += 1

        

        
        print(f'------ {cont_apagados} que ja existiam foram apagados.')
        print(f'------ {len(lista_nova)} links seram retornados para coleta de dados de anuncio.')
        lista_para_armazenar = lista_armazenada + lista_nova
        print(f'------ A nova lista armazenada tem {len(lista_para_armazenar)} links.')
        cria_json('links_lst.json', lista_para_armazenar)
    else:
        cria_json('links_lst.json', lista_nova)
            
    return lista_nova   

def innerHTML(element):
    return element.encode_contents()

def captura_dados_anuncio(soup, tipo):
    contador = 0
    while True:
        dados_anuncio = {}
        classe = soup.find_all('div', class_='sc-hmzhuo')
        for c in classe:
            if c.find('dt'):
                dt_ = c.find('dt')
                if dt_.text == tipo:
                    if c.find('dd'):
                        dados_anuncio[tipo] = c.find('dd').text
                        return dados_anuncio
                    else:
                        if c.find('a'):
                            dados_anuncio[tipo] = c.find('a').text
                            return dados_anuncio
        if contador == 5:
            dados_anuncio[tipo] = 'N/A'
            break

def captura_valor(soup):
   
    dados_anuncio = {}
    classe = soup.find_all('div', class_='sc-hmzhuo')
    for c in classe:
        if c.find('h2'):
            dados_anuncio["valor"] = c.find('h2').text
            return dados_anuncio

def captura_data(soup):
    dados_anuncio = {}
    classe = soup.find_all('div', class_='sc-hmzhuo')
    for c in classe:
        if c.find('span'):
            if 'Publicado' in c.find('span').text:
                split = c.find('span').text.split()[2]
                dados_anuncio['Data'] = split
                return dados_anuncio

def cria_json(nome_saida, fonte):
    import json

    open(nome_saida,'w').write(json.dumps(fonte))

def carrega_json(arquivo):
    import json

    arquivo_ = str(arquivo)
    with open(arquivo_, 'r') as file_json:
        anuncios = json.loads(file_json.read())
    return anuncios            

def coleta_anuncios(lista_links):
    from bs4 import BeautifulSoup
    from lxml import etree
    import requests
    import time
    import os.path
        
    if os.path.isfile('dados_anuncios_capturados.json'):
        anuncios = carrega_json('dados_anuncios_capturados.json')
        print(f'===== Qtd de anunciosarmazenados: {len(anuncios)}')
    else:
        anuncios = []

    cont = 0
    for link in lista_links:
        inicio = time.time()
        cont += 1
        
            
            
        URL = getUrl(link)
        
        print(f'>>> {cont} - Lendo > {link}')
       
        HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                    (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
                    'Accept-Language': 'en-US, en;q=0.5'})
        webpage = requests.get(link, headers=HEADERS)
        soup = BeautifulSoup(webpage.content, "html.parser")
        dom = etree.HTML(str(soup))


        dados_anuncio = {}
        
        marca = captura_marca(soup)
        marca_dct = {'Marca': marca}
        dados_anuncio.update(marca_dct)

        modelo = captura_dados_anuncio(soup, 'Modelo')
        dados_anuncio.update(modelo)

        cilindrada = captura_dados_anuncio(soup, 'Cilindrada')
        dados_anuncio.update(cilindrada)

        try:
            ano = captura_dados_anuncio(soup, 'Ano')
            dados_anuncio.update(ano)
        except:
            dados_anuncio.update({'Ano' : 'N/A'})

        try:
            km = captura_dados_anuncio(soup, 'Quilometragem')
            dados_anuncio.update(km)
        except:
            dados_anuncio.update({'Quilometragem' : 'N/A'})

        cidade = captura_dados_anuncio(soup, 'Município')
        dados_anuncio.update(cidade)

        valor = captura_valor(soup)
        numeros = ''
        for caractere in valor['valor']:
            if caractere.isdigit():
                numeros += caractere
        preco = int(numeros)
        valor_dct = {'Valor': preco}
        dados_anuncio.update(valor_dct)

        data = captura_data(soup)
        dados_anuncio.update(data)

        codigo = link[-12::].split('-')[1]
        dct_codigo = {'Codigo': codigo}
        dados_anuncio.update(dct_codigo)

        url = {'Url': link}
        dados_anuncio.update(url)

        
        anuncios.append(dados_anuncio)
        if cont % 50 == 0:
            print('Dormindo por 15 segundos!')
            time.sleep(15)
        

        cria_json('dados_anuncios_capturados.json', anuncios)
        fim = time.time()
        tempo = fim - inicio
        print(F'   >>> CAPTURADO EM: {tempo} seg.') 
        print('') 
    print(f'===== Nova qtd de anuncios: {len(anuncios)}')
    print(len(anuncios))
    return anuncios
    

def captura_marca(soup):
   
    classe = soup.find('title')
    return classe.text.split(' ')[0]
