import pandas as pd
import time
import streamlit as st
import plotly.express as px


#==============================Decorador==============================#

def monitorar_tempo(funçao_alvo):

    def embrulho(*args,**kwargs):
        tempo_inicio = time.time()
        resultado = funçao_alvo(*args, **kwargs)
        tempo_final = time.time()
        tempo_resultado = tempo_final - tempo_inicio
        print(tempo_resultado)
        return resultado
    return embrulho

@monitorar_tempo
@st.cache_data

def ler_csv():
    df = pd.read_csv('Performance de Qualidade.csv', sep = ';')
    return df
dados_bd = ler_csv()

dados_bd = dados_bd.fillna(0)

tabela_final = dados_bd

#=========================Organização de dados==========================#

nomes_sup = dados_bd['Nome Super'].unique().tolist()
nomes_sup.insert(0, 'Todos')

ano_sup = dados_bd['Ano'].unique().tolist()
ano_sup.insert(0, 'Todos')

mes_sup = dados_bd['Mês'].unique().tolist()
mes_sup.sort()
mes_sup.insert(0, 'Todos')

#===========================Streamlit Visual===========================#

st.set_page_config(
    page_title = 'Performance de Qualidade',
    page_icon = '📊',

)
st.title('Bem vindo(a) ao Performance de Qualidade 📊')

#=====================Filtros para o que Visualizar=====================#

filtros_nome_sup = st.sidebar.selectbox('Selecione um Supermercado', nomes_sup)

if 'Todos' != filtros_nome_sup:
    tabela_final = tabela_final[tabela_final['Nome Super'] == filtros_nome_sup]


filtros_ano_sup = st.sidebar.selectbox('Selecione um Ano', ano_sup)

if 'Todos' != filtros_ano_sup:
    tabela_final = tabela_final[tabela_final['Ano'] == filtros_ano_sup]


filtros_mes_sup = st.sidebar.selectbox('Selecione um Mês', mes_sup)

if 'Todos' != filtros_mes_sup:
    tabela_final = tabela_final[tabela_final['Mês'] == filtros_mes_sup]

#=====================Limpeza de Dados p/ Graficos======================#

tabela_final['Periodo'] = tabela_final['Ano'].astype(str) + '-' + tabela_final['Mês'].astype(str)

tabela_final['Pago a Maior ICMS'] = tabela_final['Pago a Maior ICMS'].str.replace(',', '.').astype(float)

tabela_final['Pago a Menor ICMS'] = tabela_final['Pago a Menor ICMS'].str.replace(',', '.').astype(float)

tabela_final['Risco PIS'] = tabela_final['Risco PIS'].str.replace(',', '.').astype(float)

tabela_final['Risco COFINS'] = tabela_final['Risco COFINS'].str.replace(',', '.').astype(float)

tabela_agrupada = tabela_final.groupby(['Periodo'])[['Pago a Maior ICMS', 'Pago a Menor ICMS', 'Risco PIS', 'Risco COFINS']].sum().reset_index()

tabela_agrupada['Periodo'] = pd.to_datetime(tabela_agrupada['Periodo'])

tabela_agrupada = tabela_agrupada.sort_values(by='Periodo')

tabela_agrupada['Risco Consolidado'] = tabela_agrupada['Risco PIS'] + tabela_agrupada['Risco COFINS']

#===========================Graficos Tratatados===========================#

grafico_barra = px.bar(tabela_agrupada, x = 'Periodo', y = ['Pago a Maior ICMS','Pago a Menor ICMS'], text_auto=True)
grafico_linhas = px.line(tabela_agrupada, x = 'Periodo', y = ['Risco Consolidado'])

st.plotly_chart(grafico_barra)
st.plotly_chart(grafico_linhas)

tabela_final['Total Impacto'] = tabela_final['Pago a Maior ICMS'] + tabela_final['Pago a Menor ICMS'] + tabela_final['Risco PIS'] + tabela_final['Risco COFINS']

mercados_criticos = tabela_final[tabela_final['Total Impacto'] > 100000]

grafico_pizza = px.pie(mercados_criticos, names = 'Nome Super', values = 'Total Impacto')
st.plotly_chart(grafico_pizza)
