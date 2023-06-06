import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
#import matplotlib.pyplot as plt
from datetime import date
#from PIL import Image
import time

st.set_page_config(
    page_title="Página inicial / Commodities",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
    }
)

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)  

st.title("DASHBOARD DAS :blue[COMMODITIES]")

#       ordem das commodites no array: ouro, prata, platina, cobre, pretoleo cru, gas natural e café. 
lista_commodities = ['GC=F', 'SI=F', 'PL=F', 'HG=F', 'CL=F', 'NG=F', 'KC=F', 'CB=F', 'CT=F']

#       recebendo a data do input
with st.sidebar:
    st.title(':blue[FILTRO]')
    data_inicio=st.date_input("Escolha a data inicial:", datetime.date(2023, 1, 1))
    data_fim=st.date_input("Escolha a data final:", date.today())
    st.divider()

#       fazendo download dos valores via yfinance
commodities_tudo=yf.download(lista_commodities, start=data_inicio, end=data_fim)['Adj Close']

#       renomeando as commodities
r_pd_commodities_tudo=pd.DataFrame(commodities_tudo.rename(columns={'CL=F':'Petroleo Cru', 'GC=F':'Ouro', 'HG=F':'Cobre', 'KC=F':'Café', 'NG=F':'Gás natural', 
                                                                    'PL=F':'Platina', 'SI=F':'Prata', 'CT=F':'Algodão', 'CB=F': 'Açúcar'}))
#       tirando a hora '00:00:00' da coluna 'Date'
r_pd_commodities_tudo.index=r_pd_commodities_tudo.index.date

tab1, tab2, tab3 = st.tabs(["📈 Gráfico", " 🙅‍♂️ Correlação", "✅ Correlação selecionada"])

with tab1:
    st.header("LISTAGEM")
    r_pd_commodities_tudo

    st.divider()
    
    #       plotando
    st.header("GRÁFICO")
    st.line_chart(r_pd_commodities_tudo)

    with st.expander("Ver explicação"):
        st.write("O gráfico acima mostra a variação de preço (em :green[U$]), das :blue[COMMODITIES].")
        
with tab2:
    st.header("CORRELAÇÃO")

    #       mostrando o dataframe da correlação
    st.dataframe(r_pd_commodities_tudo.corr())

    with st.expander("Ver explicação"):
        st.write("O DataFrame acima mostra a correlação das :blue[COMMODITIES].")

with tab3:
    st.header("CORRELAÇÃO SELECIONADA")
    st.write("Selecione pelo menos 2 :blue[COMMODITIES] para correlação!")
    #   adicionando espaço vazio
    st.text("")
    st.text("")
    #   adicionando varias colunas para poder alinhas a direita
    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)

    with col1:
        selOuro = st.checkbox('Ouro')        
    with col2: 
        selPrata = st.checkbox('Prata')
    with col3:
        selPlatina = st.checkbox('Platina')
            
    if selOuro and selPrata:
        lista_sel=['GC=F', 'SI=F']
        commodities_corr=yf.download(lista_sel, start=data_inicio, end=data_fim)['Adj Close']
        r_commodities_corr=pd.DataFrame(commodities_corr.rename(columns={'GC=F': 'Ouro', 'SI=F':'Prata'}))
        st.dataframe(r_commodities_corr.corr())

    elif selOuro and selPlatina:
        lista_sel2=['GC=F', 'PL=F']
        commodities_corr=yf.download(lista_sel2, start=data_inicio, end=data_fim)['Adj Close']
        r_commodities_corr2=pd.DataFrame(commodities_corr.rename(columns={'GC=F': 'Ouro', 'PL=F':'Platina'}))
        st.dataframe(r_commodities_corr2.corr())


    elif selPrata and selPlatina:
        lista_sel3=['SI=F', 'PL=F']
        commodities_corr=yf.download(lista_sel3, start=data_inicio, end=data_fim)['Adj Close']
        r_commodities_corr3=pd.DataFrame(commodities_corr.rename(columns={'SI=F': 'Prata', 'PL=F':'Platina'}))
        st.dataframe(r_commodities_corr3.corr())
    
    elif selPrata and selPlatina and selOuro:
        lista_sel4=['SI=F', 'PL=F', 'GC=F']
        commodities_corr=yf.download(lista_sel4, start=data_inicio, end=data_fim)['Adj Close']
        r_commodities_corr4=pd.DataFrame(commodities_corr.rename(columns={'SI=F': 'Prata', 'PL=F':'Platina', 'GC=F':'Ouro'}))
        st.dataframe(r_commodities_corr4.corr())

    else:
        st.divider()
        #   fazendo o 'invalido' desaparecer dps de 3 segundos
        with st.empty():
            for seconds in range(3):
                st.markdown('<p class="red-color">INVÁLIDO!</p>', unsafe_allow_html=True)
                time.sleep(1)
            st.write("")
