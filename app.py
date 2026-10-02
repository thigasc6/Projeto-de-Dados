import pandas as pd
import time
import streamlit as st
import plotly.express as px


#==============================Decorador==============================#

def monitorar_tempo(funçao_alvo):

    def embrulho(*args,**kwargs):
        resultado = funçao_alvo(*args, **kwargs)
        return resultado
    return embrulho

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

if tabela_final.empty:
    st.warning('Nenhum dado encontrado para os filtros selecionados.')
    st.stop()

#=====================Limpeza de Dados p/ Graficos======================#

tabela_final['Periodo'] = tabela_final['Ano'].astype(str) + '-' + tabela_final['Mês'].astype(str)

tabela_final['Pago a Maior ICMS'] = tabela_final['Pago a Maior ICMS'].str.replace(',', '.').astype(float)

tabela_final['Pago a Menor ICMS'] = tabela_final['Pago a Menor ICMS'].str.replace(',', '.').astype(float)

tabela_final['Risco PIS'] = tabela_final['Risco PIS'].str.replace(',', '.').astype(float)

tabela_final['Risco COFINS'] = tabela_final['Risco COFINS'].str.replace(',', '.').astype(float)

tabela_agrupada = tabela_final.groupby(['Periodo'])[['Pago a Maior ICMS', 'Pago a Menor ICMS', 'Risco PIS', 'Risco COFINS']].sum().reset_index()

tabela_agrupada['Periodo'] = pd.to_datetime(tabela_agrupada['Periodo'])

tabela_agrupada = tabela_agrupada.sort_values(by='Periodo')

#===========================Graficos Tratatados===========================#

grafico_barra = px.bar(tabela_agrupada, x = 'Periodo', y = ['Pago a Maior ICMS','Pago a Menor ICMS'], text_auto=True)

st.subheader('Risco de ICMS Pag. a Maior e Pag. a Menor')

st.plotly_chart(grafico_barra)

#==========================================================================#

grafico_linhas = px.line(tabela_agrupada, x = 'Periodo', y = ['Risco PIS', 'Risco COFINS'])

st.subheader('Risco Pis e Cofins')

st.plotly_chart(grafico_linhas)

#==========================================================================#

tabela_final['Faturamento Sup.'] = tabela_final['Faturamento Sup.'].str.replace(',','.').astype(float)

top10agrupados = tabela_final.groupby(['Nome Super'])[['Faturamento Sup.']].sum().reset_index()

maioresfat =  top10agrupados.nlargest(10,'Faturamento Sup.')

grafico_top10 = px.pie(maioresfat, names = 'Nome Super', values = 'Faturamento Sup.')

st.subheader('Top 10 Maiores Faturamentos ')

st.plotly_chart(grafico_top10)


#==========================================================================#

tabela_final['Faturamento Pad.'] = tabela_final['Faturamento Pad.'].str.replace(',','.').astype(float)

top10pad_agrupados = tabela_final.groupby(['Nome Super'])[['Faturamento Pad.']].sum().reset_index()

maioresfat_pad = top10pad_agrupados.nlargest(10, 'Faturamento Pad.')

grafico_top10_pad = px.pie(maioresfat_pad, names = 'Nome Super', values = 'Faturamento Pad.')

st.subheader('Top 10 Faturamento Padaria')

st.plotly_chart(grafico_top10_pad)