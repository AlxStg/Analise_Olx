from pack import *
from bs4 import BeautifulSoup
from lxml import etree
import requests
import time


inicio = time.time()

links_coletados = coletaLinks()

links_analisar = exclui_links_existentes(links_coletados)

anuncios_coletados = coleta_anuncios(links_analisar)


fim = time.time()
tempo = fim - inicio
if tempo > 60:
    tempo_decorrido_minutos = (fim - inicio)/60
    print(F' >>>>>>>>>>>  TEMPO DE EXECUÇÃO: {tempo_decorrido_minutos} min.')   
else:
    print(F' >>>>>>>>>>>  TEMPO DE EXECUÇÃO: {tempo} seg.')

    
    
