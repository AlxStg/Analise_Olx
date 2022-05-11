

def coleta_links_anuncios():
    import os.path
    import time

    inicio_coleta = time.time() 

    if os.path.isfile('links_lst.json'):
        print('>>>>>>>>> Já existe uma lista de arquivos armazenada!')
        opt_carregar_links = 0
        while True:
            opt_carregar_links = int(input('Digite 1 para carregar os links salvos ou 2 para carregar nova lista de links: '))
            if opt_carregar_links == 1:
                print('>>>>>>>>> CARREGANDO A LISTA EXISTENTE!!!')
                lista_links = carrega_json('links_lst.json')
                fim_coleta = time.time()
                tempo = fim_coleta - inicio_coleta
                print(F'---->  TEMPO: {tempo} seg.')
                break
            if opt_carregar_links == 2:
                print('>>>>>>>>> CARREGANDO NOVA LISTA !!!')
                lista_links = coletaLinks()
                cria_json('links_lst.json', lista_links)
                fim_coleta = time.time()
                tempo = fim_coleta - inicio_coleta
                print(F'---->  TEMPO: {tempo} seg.')
                break
            else:
                print('>>> ERRO --> Opção inválida!')
        return lista_links

    else:
        print('>>>>>>>>> Não existe uma lista de arquivos armazenada!\n >>>>>>>> CARREGANDO NOVA LISTA!')
        lista_links = coletaLinks()
        cria_json('links_lst.json', lista_links)
        return lista_links
    
def getUrl(paginacao):
    return "https://mg.olx.com.br/belo-horizonte-e-regiao/autos-e-pecas/motos?o="+str(paginacao)+"&pe=11000&ps=2000&re=39&rs=18"

def innerHTML(element):
    """Returns the inner HTML of an element as a UTF-8 encoded bytestring"""
    return element.encode_contents()

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
    
    print('=' * 100)
    print(f'   >>>>> {opt} paginas percorridas.\n   >>>>> {cont} links de anuncio capturados.')
    print('=' * 100)
    return links   

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
    
    

    anuncios = []
    cont = 0
    for link in lista_links:
        inicio = time.time()
        cont += 1
        if cont % 50 == 0:
            print('Dormindo por 10 segundos!')
            time.sleep(10)
            
        URL = getUrl(link)
        print('')
        print('')
        print(f'>>> {cont} - Lendo > {link}')
        print('')
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
        print(f'Marca: {dados_anuncio["Marca"]}')

        modelo = captura_dados_anuncio(soup, 'Modelo')
        dados_anuncio.update(modelo)
        print(f'Modelo: {dados_anuncio["Modelo"]}')

        cilindrada = captura_dados_anuncio(soup, 'Cilindrada')
        dados_anuncio.update(cilindrada)
        print(f'Cilindrada: {dados_anuncio["Cilindrada"]}')

        try:
            ano = captura_dados_anuncio(soup, 'Ano')
            dados_anuncio.update(ano)
        except:
            dados_anuncio.update({'Ano' : 'N/A'})
        print(f'Ano: {dados_anuncio["Ano"]}')

        try:
            km = captura_dados_anuncio(soup, 'Quilometragem')
            dados_anuncio.update(km)
        except:
            dados_anuncio.update({'Quilometragem' : 'N/A'})
        print(f'Quilometragem: {dados_anuncio["Quilometragem"]}')

        cidade = captura_dados_anuncio(soup, 'Município')
        dados_anuncio.update(cidade)
        print(f'Município: {dados_anuncio["Município"]}')

        valor = captura_valor(soup)
        numeros = ''
        for caractere in valor['valor']:
            if caractere.isdigit():
                numeros += caractere
        preco = int(numeros)
        valor_dct = {'Valor': preco}
        dados_anuncio.update(valor_dct)
        print(f'Valor: {dados_anuncio["Valor"]}')

        data = captura_data(soup)
        dados_anuncio.update(data)
        print(f'Data: {dados_anuncio["Data"]}')

        codigo = link[-12::].split('-')[1]
        dct_codigo = {'Codigo': codigo}
        dados_anuncio.update(dct_codigo)
        print(f'Código: {dados_anuncio["Codigo"]}')

        url = {'Url': link}
        dados_anuncio.update(url)
        print(f'Url: {dados_anuncio["Url"]}')

        
        anuncios.append(dados_anuncio)
        cria_json('dados_anuncios_capturados.json', anuncios)
        fim = time.time()
        tempo = fim - inicio
        print(F'\n >>> CAPTURADO EM: {tempo} seg.') 
          

    return anuncios

def captura_marca(soup):
   
    classe = soup.find('title')
    return classe.text.split(' ')[0]
