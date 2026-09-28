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

#=====================================================================#

nomes_sup = dados_bd['Nome Super'].unique().tolist()

nomes_sup.insert(0, 'Todos')

ano_sup = dados_bd['Ano']

ano_sup.insert(0, 'todos')
               
#=====================================================================#


st.title('Testeee')
filtros_nome_sup = st.sidebar.selectbox('Selecione uma opção', nomes_sup)
filtros_ano_sup = st.sidebar.selectbox('Selecione um ano', ano_sup)


if filtros_nome_sup == 'Todos':
    st.bar_chart(dados_bd[['Pago a Maior ICMS','Pago a menor ICMS']])
else:
    st.dataframe(dados_bd['Nome Super'])

