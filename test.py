import pandas as pd

print(pd.read_html('https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-de-segmentos-e-setoriais/indice-agronegocio-free-float-setorial-agfs-composicao-da-carteira.htm', attrs = {'class': 'table table-responsive-sm table-responsive-md'}))