# Métodos referentes á captura de dados:

import json


def getUrl(paginacao):
    return "https://mg.olx.com.br/belo-horizonte-e-regiao/autos-e-pecas/motos?o="+str(paginacao)+"&pe=10000&ps=2000&re=39&rs=22&sf=1"

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
        print(f'------ {len(lista_nova)} links serão retornados para coleta de dados de anuncio.')
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
        if (cont - 1) % 50 == 0:
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




# Métodos referentes à análise de dados:
def converte_csv_json(fonte_csv, destino_json):
    import csv
    import json

    jsonFilePath = destino_json

    dados = []

    # Abre e lê o arquivo csv
    with open(fonte_csv, 'r') as csvFile:
        csvReader = csv.DictReader(csvFile)
        for rows in csvReader:
            dados.append(rows)
        print('CONVERSÃO BEM SUCEDIDA!')
    # Cria o arquivo json
    with open(jsonFilePath, 'w') as jsonFile:
        jsonFile.write(json.dumps(dados, indent=4))

def corrige_dados_fipe(json_fipe):
    for x in range(0,10):
        arquivo = carrega_json(json_fipe)
        # Apaga dados desnecessários da lista fipe:
        try:
            for c in arquivo:
                try:
                    del c["Combustivel"]
                except:
                    pass
                try:
                    del c["MesReferencia"]
                except:
                    pass
                try:
                    del c["Autenticacao"]
                except:
                    pass
                try:
                    del c["TipoVeiculo"]
                except:
                    pass
                try:
                    del c["SiglaCombustivel"]
                except:
                    pass
                try:
                    del c["DataConsulta"]
                except:
                    pass

                try:
                    c["id"] = c["Modelo"]
                    del c["Modelo"]
                except:
                    pass

                try:
                    c["Ano"] = c["AnoModelo"]
                    del c["AnoModelo"]
                except:
                    pass

                try:
                    c["Codigo Fipe"] = c["CodigoFipe"]
                    del c["CodigoFipe"]
                except:
                    pass

                try:
                    valor_cor = c["Valor"].split(",")[0]
                    c["Valor"] = valor_cor
                except:
                    pass

                if c["Marca"] not in c["id"]:
                    new = f'{c["Marca"]} - {c["id"]}'
                    c["id"] = new 

        except:
            pass

           
    



    cria_json(json_fipe, arquivo)
    print(' >>>=======> CORREÇÕES PRÉ-DEFINIDAS REALIZADAS COM SUCESSO!')

def compara_ano(fonte_fipe, fonte_olx):
    
    lista = []
    contador = 0
    for c in fonte_fipe:
        if str(c['Ano']) == str(fonte_olx['Ano']):
            lista.append(contador)
        contador += 1 
    return lista

def compara_marca(lista_ano, fonte_fipe, anuncio):
    
    lista_resultado = []
    for c in lista_ano:
        if fonte_fipe[c]['Marca'] == anuncio['Marca']:
            lista_resultado.append(c)
    return lista_resultado

def best_match_fipe(anuncio, lista_marca, fipes):
    # Encontrar melhor resultado por id:
                    
                    ## Compara quantas palavras do id do anuncio coincidem no fipe:
                    lista_com_pts = []
                    mod_an_quebr = anuncio['Modelo'].split()
                    for c in lista_marca:
                        pontos_no_id = {}
                        pts_mod = 0
                        for palavra in mod_an_quebr:
                            if palavra in fipes[c]['id']:
                                pts_mod += 1
                        pontos_no_id["posicao"] = c                             
                        pontos_no_id['pts'] = pts_mod
                        lista_com_pts.append(pontos_no_id)

                    ## Encontra maior pontuação
                    match_fipe = []
                    maior_pts = 0
                    for c in lista_com_pts:
                        if c['pts'] > maior_pts:
                            maior_pts = c['pts']
                    
                    for c in lista_com_pts:
                        if c['pts'] == maior_pts:
                            match_fipe.append(c['posicao'])
                    return match_fipe

def best_match_fipe_2(anuncio, lista_marca, fipes):
    # Encontrar melhor resultado por id:
                    
                    ## Compara quantas palavras do id do anuncio coincidem no fipe:
                    lista_com_pts = []
                    url_split = anuncio['Url'].split()
                    mod_an_quebr = anuncio['Url'].split()
                    for c in lista_marca:
                        pontos_no_id = {}
                        pts_mod = 0
                        for palavra in mod_an_quebr:
                            if palavra in fipes[c]['id']:
                                pts_mod += 1
                        pontos_no_id["posicao"] = c                             
                        pontos_no_id['pts'] = pts_mod
                        lista_com_pts.append(pontos_no_id)

                    ## Encontra maior pontuação
                    match_fipe = []
                    maior_pts = 0
                    for c in lista_com_pts:
                        if c['pts'] > maior_pts:
                            maior_pts = c['pts']
                    
                    for c in lista_com_pts:
                        if c['pts'] == maior_pts:
                            match_fipe.append(c['posicao'])
                    return match_fipe


def list_cods_fipe (melhor_resultado, fipes):

    lst_cod_fipe = []
    for c in melhor_resultado:
        dict_cods_fipe = {} 
        cod = fipes[c]['Codigo Fipe']
        
        numeros = ''
        for caractere in fipes[c]['Valor']:
            if caractere.isdigit():
                numeros += caractere
        valor = int(numeros)

        dict_cods_fipe["Codigo"] = cod
        dict_cods_fipe["id"] = fipes[c]['id']
        dict_cods_fipe["Valor"] = valor
        lst_cod_fipe.append(dict_cods_fipe)


    return lst_cod_fipe

def cruza_dados():
    contador = 0
    anuncios = carrega_json('dados_anuncios_capturados.json')
    fipes = carrega_json('dados_fipe.json')
    
    for anuncio in anuncios:
        contador += 1
        if contador % 10 == 0:
            print(f'>>>>>>>>>>> {contador} de {len(anuncios)}')
        lista_ano = compara_ano(fipes, anuncio)
        lista_marca = compara_marca(lista_ano, fipes, anuncio)
        melhor_resultado = best_match_fipe(anuncio, lista_marca, fipes)
        anuncio['cod_fipe'] = list_cods_fipe(melhor_resultado, fipes)
        anuncio['valor_fipe'] = 0

    cria_json('dados_anuncios_capturados.json' , anuncios)

def contador_fipes_em_anuncios():
    
    anuncios = carrega_json('dados_anuncios_capturados.json')
    
    cont_fipe_atribuido = 0
    cont_fipe_unico = 0
    cont_fipe_duplo = 0
    cont_fipe_multiplo = 0
    cont_sem_fipe = 0
    for c in anuncios:
        if c['valor_fipe'] > 0:
            cont_fipe_atribuido += 1
        if len(c['cod_fipe']) == 1:
            c['valor_fipe'] = c['cod_fipe'][0]['Valor']
            cont_fipe_unico += 1
        if c['valor_fipe'] == 0 and len(c['cod_fipe']) == 2:
            cont_fipe_duplo += 1
        if c['valor_fipe'] == 0 and len(c['cod_fipe']) >2:
            cont_fipe_multiplo += 1
        if len(c['cod_fipe']) == 0:
            cont_sem_fipe += 1
            
            
    print('§ ' * 45)
    print(f'=====> {cont_fipe_atribuido:_^6} com valor fipe atribuido.')    
    print(f'=====> {cont_fipe_unico:_^6} com 1 cód. fipe associado.')
    print(f'=====> {cont_fipe_duplo:_^6} com 2 fipes associados.')
    print(f'=====> {cont_fipe_multiplo:_^6} com MULTIPLOS códs. fipes associados.')
    if cont_sem_fipe > 0:
        print(f'=====> {cont_sem_fipe:_^6} NÃO TEM códs. fipes associados.')
    print('§ ' * 45)
    print('')

def correcao_automatica_cod_fipe_em_anuncios():
    anuncios = carrega_json('dados_anuncios_capturados.json')
    fipes = carrega_json('dados_fipe.json')
    
    

    print('>>>>> Tentando executar correções automaticamente')
    print('')
    for c in anuncios:
        if len(c['cod_fipe']) == 1:
            c['valor_fipe'] = c['cod_fipe'][0]['Valor']
        
        if len(c['cod_fipe']) == 2:
            media = (c['cod_fipe'][0]['Valor'] + c['cod_fipe'][1]['Valor']) / 2
            if c['cod_fipe'][0]['Valor'] > c['cod_fipe'][1]['Valor']:
                diferenca = ((c['cod_fipe'][0]['Valor'] - media) / c['cod_fipe'][0]['Valor']) * 100
            else:
                diferenca = ((c['cod_fipe'][1]['Valor'] - media) / c['cod_fipe'][1]['Valor']) * 100
            if diferenca <= 6.2:
                c["valor_fipe"] = media

    cria_json('dados_anuncios_capturados.json' , anuncios)    

def exibe_anuncio_p_correcao():
    anuncios = carrega_json('dados_anuncios_capturados.json')
    fipes = carrega_json('dados_fipe.json')
    contador = 0
    for y in anuncios:
        

        if y['valor_fipe'] == 0:
            print('')
            print('§' * 100)
            print(f"Url: {y['Url']}")
            print(f"Marca: {y['Marca']}")
            print(f"Modelo: {y['Modelo']}")
            print(f"Cilindrada: {y['Cilindrada']}")
            print(f"Ano: {y['Ano']}")
            print('.' * 80)
            print('-=-=-=- Códs. fipe associados. -=-=-=-')
            
            cont_cod = 0
            for z in y['cod_fipe']:
                cont_cod += 1
                print(f"-= {cont_cod} =- : {z['id']}")
            print(
            '''
            1. Escolher a partir dos existentes;
            2. Inserir ValorFipe manualmente.
            3. Apagar anuncio;
            4. Skip;
            5. Voltar.
            '''
            )
            opt = int(input('>>>>> Opção: '))
            
            if opt == 1:
                opt_cod = int(input('Fipe correspondente: ')) - 1
                y['valor_fipe'] = y['cod_fipe'][opt_cod]['Valor']
                print(f">>>>>> ALTERADO - {y['cod_fipe'][opt_cod]['id']}")

            if opt == 2:
                valor_fipe_manual = int(input('Valor: '))
                y['valor_fipe'] = valor_fipe_manual
                print(f'>>>>>> ALTERADO - {y["valor_fipe"]}')





            if opt == 3:
                del anuncios[contador]
                print('>>> APAGAR')
                
                


            if opt == 4:
                pass

            



            cria_json('dados_anuncios_capturados.json' , anuncios)
            print("===> Confirmado")

        contador += 1

def cria_diferenca_fipe():
    anuncios = carrega_json('dados_anuncios_capturados.json')
    try:
        for i in anuncios:
            diferença_fipe = i['valor_fipe'] - i['Valor']
            i['diferença_fipe'] = diferença_fipe
            cria_json('dados_anuncios_capturados.json' , anuncios)
            print("===> Confirmado")
    except:
        print ("NUM DEU!!")
        pass

def exporta_csv():
    import csv

    anuncios = carrega_json('dados_anuncios_capturados.json')
    header = ['Modelo', 'Cilindrada', 'Ano', 'Valor', 'valor_fipe', 'Url', 'Codigo', 'cod_fipe', 'Data', 'Marca', 'Quilometragem', 'diferença_fipe', 'Município']
    try:
        with open('anuncios_tratados.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            for elem in anuncios:
                writer.writerow(elem)
        print('>>>> ARQUIVO .csv CRIADO COM SUCESSO! <<<')
    except IOError:
        print("I/O error")



