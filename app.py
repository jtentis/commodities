import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from datetime import date
from PIL import Image

st.set_page_config(
    page_title="Commodities",
    page_icon="📈",
    #layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
    }
)

#ordem das commodites no array: ouro, prata, platina, cobre, pretoleo cru, gas natural e café. 
lista_commodities = ['GC=F', 'SI=F', 'PL=F', 'HG=F', 'CL=F', 'NG=F', 'KC=F']

st.title("DASHBOARD DAS COMMODITIES")

#recebendo a data do input
data_inicio=st.date_input("Escolha a data inicial:", datetime.date(2020, 1, 1))
data_fim=st.date_input("Escolha a data final:", date.today())
commodities_tudo=yf.download(lista_commodities, start=data_inicio, end=data_fim)['Adj Close']

tab1, tab2, tab3 = st.tabs(["📈 Gráfico", " 💹 Correlação", "Correlação selecionada"])

with tab1:
    st.header("GRÁFICO")

    #plotando
    st.line_chart(commodities_tudo)

    with st.expander("Ver explicação"):
        st.write("O gráfico acima mostra a variação de preço (em U$), das seguintes :blue[commodities]: ouro, prata, platina, cobre, pretoleo cru, gas natural e café.")
        #imagem=Image.open('/home/jtentis/Documentos/projetos/commodities/imagens/commodities.png')
        #st.image(imagem, width=300)
        

with tab2:
    st.header("CORRELAÇÃO")

    #mostrando o dataframe da correlação
    st.dataframe(commodities_tudo.corr())

    with st.expander("Ver explicação"):
        st.write("O dataframe acima mostra a correlação das :blue[commodities].")

with tab3:
    st.header("CORRELAÇÃO SELECIONADA")
    st.subheader("Selecione pelo menos 2 :blue[commodities] para correlação!")

    selOuro = st.checkbox('Ouro')
    selPrata = st.checkbox('Prata')
    selPlatina = st.checkbox('Platina')

    if selOuro and selPrata:
        commodities_corr=['GC=F', 'SI=F']
        commodities_corr=yf.download(commodities_corr, start=data_inicio, end=data_fim)['Adj Close']
        st.dataframe(commodities_corr.corr()) 

    elif selOuro and selPlatina:
        commodities_corr2=['GC=F', 'PL=F']
        commodities_corr2=yf.download(commodities_corr2, start=data_inicio, end=data_fim)['Adj Close']
        st.dataframe(commodities_corr2.corr())

    elif selPrata and selPlatina:
        commodities_corr3=['SI=F', 'PL=F']
        commodities_corr3=yf.download(commodities_corr3, start=data_inicio, end=data_fim)['Adj Close']
        st.dataframe(commodities_corr3.corr())
    
    elif selPrata and selPlatina and selOuro:
        commodities_corr4=['GC=F', 'SI=F', 'PL=F']
        commodities_corr4=yf.download(commodities_corr4, start=data_inicio, end=data_fim)['Adj Close']
        st.dataframe(commodities_corr4.corr())

    else:
        st.divider()
        st.write("INVÁLIDO!")
