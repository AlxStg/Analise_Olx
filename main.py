from pack import *
from bs4 import BeautifulSoup
from lxml import etree
import requests
import time

while True:
    print('')
    print('$$' * 25)
    print(f"{'OLX vs FIPE':^50}")
    print('$$' * 25)
    print('')
    print(
    f'''
        - MENU PRINCIPAL 

        1. Captura de dados;
        2. Analise de Dados;
        3. Fechar.
    '''
    )
    opt_menu = int(input(' - Opção: '))

    if opt_menu == 1:
        # Captura de dados dos anuncios e cria arquivo ".json" com os dados:
        print('')
        print('--' * 25)
        print(f"{'- CAPTURA DE DADOS -':^50}")
        print('--' * 25)
        print('')
        inicio = time.time()
        links_coletados = coletaLinks()
        links_analisar = exclui_links_existentes(links_coletados)
        anuncios_coletados = coleta_anuncios(links_analisar)
        fim = time.time()
        tempo = fim - inicio
        if tempo > 60:
            tempo_decorrido_minutos = (fim - inicio)/60
            print(F' >>>>>>>>>>>  TEMPO DE EXECUÇÃO(Captura de dados): {tempo_decorrido_minutos} min.')   
        else:
            print(F' >>>>>>>>>>>  TEMPO DE EXECUÇÃO(Captura de dados): {tempo} seg.')

    if opt_menu == 2:
        while True:
            
            print('')
            print('--' * 25)
            print(f"{'- MENU DE ANÁLISE -':^50}")
            print('--' * 25)
            print('')
            print(
                f'''
                1. Carregar e converter arquivo FIPE ".csv";

                2. Executar correções no arquivo FIPE;

                3. Executar cruzamento de listas;

                4. AnalizaR corrigir eventuais erros de cruzamento;

                5. Exportar lista cruzada para ".csv";

                6. Voltar ao menu principal.

                '''
                )
            opt_menu_analise = int(input(' - Opção: '))

            if opt_menu_analise == 1:

                converte_csv_json("dados_fipe.csv", 'dados_fipe.json')
                print('\n ------ Arquivo carregado e convertido')
                
                
            if opt_menu_analise == 2:
               
                corrige_dados_fipe("dados_fipe.json")
        










    if opt_menu == 3:
        print('$'*50)
        print(f"{'PROGRAMA ENCERRADO ---> OBRIGADO.':^50}")
        print('$'*50)
        break

    if opt_menu not in (1,2,3):
        print('/'*50)
        print(f"{'ERRO - Opção invalida - Tente n;ovamente.':^50}")
        print('/'*50)
        

        
