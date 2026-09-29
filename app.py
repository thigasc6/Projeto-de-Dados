import pandas as pd
import streamlit as st
import time

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

#===========================Streamlit Visual===========================#

nomes_sup = dados_bd['Nome Super'].unique().tolist()
nomes_sup.insert(0, 'Todos')

ano_sup = dados_bd['Ano'].unique().tolist()
ano_sup.insert(0, 'Todos')

mes_sup = dados_bd['Mês'].unique().tolist()
mes_sup.sort()
mes_sup.insert(0, 'Todos')

#=====================================================================#

st.set_page_config(
    page_title = 'Perfomance de Qualidade',
    page_icon = '📊',

)
st.title('Bem vindo(a) ao Perfomance de Qualidade 📊')

#=====================================================================#

filtros_nome_sup = st.sidebar.selectbox('Selecione um Supermercado', nomes_sup)

if 'Todos' != filtros_nome_sup:
    tabela_final = tabela_final[tabela_final['Nome Super'] == filtros_nome_sup]


#=====================================================================#

filtros_ano_sup = st.sidebar.selectbox('Selecione um Ano', ano_sup)

if 'Todos' != filtros_ano_sup:
    tabela_final = tabela_final[tabela_final['Ano'] == filtros_ano_sup]

#=====================================================================#


filtros_mes_sup = st.sidebar.selectbox('Selecione um Mês', mes_sup)

if 'Todos' != filtros_mes_sup:
    tabela_final = tabela_final[tabela_final['Mês'] == filtros_mes_sup]

st.dataframe(tabela_final)

