from pack import *
from bs4 import BeautifulSoup
from lxml import etree
import requests
import time

inicio = time.time()

lista_links = coleta_links_anuncios()

anuncios_coletados = coleta_anuncios(lista_links)
print(anuncios_coletados)

fim = time.time()
tempo = fim - inicio
if tempo > 60:
    tempo_decorrido_minutos = (fim - inicio)/60
    print(F' >>>>>>>>>>>  TEMPO DE EXECUÇÃO: {tempo_decorrido_minutos} min.')   
else:
    print(F' >>>>>>>>>>>  TEMPO DE EXECUÇÃO: {tempo} seg.')       

    
    
