import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
#import matplotlib.pyplot as plt
from datetime import date
from PIL import Image
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
lista_commodities = ['GC=F', 'SI=F', 'PL=F', 'HG=F', 'CL=F', 'NG=F', 'KC=F', 'SB=F', 'CT=F', 'CC=F', 'ZS=F', 'ZC=F', 'LE=F', 'KE=F']

image=Image.open("imagens/cefet-logo1.png")

#       recebendo a data do input
with st.sidebar:
    st.sidebar.image(image)
    st.text("")
    st.title(':blue[FILTRO]')
    data_inicio=st.date_input("Escolha a data inicial:", datetime.date(2023, 1, 1))
    data_fim=st.date_input("Escolha a data final:", date.today())
    #st.divider()

#       fazendo download dos valores via yfinance
commodities_tudo=yf.download(lista_commodities, start=data_inicio, end=data_fim)['Adj Close']
#commodities_tudo_multi=pd.DataFrame(commodities_tudo)

#       renomeando as commodities
r_pd_commodities_tudo=pd.DataFrame(commodities_tudo.rename(columns={'CL=F':'Petroleo Cru', 'GC=F':'Ouro', 'HG=F':'Cobre', 'KC=F':'Café', 'NG=F':'Gás natural', 
                                                                    'PL=F':'Platina', 'SI=F':'Prata', 'CT=F':'Algodão', 'SB=F': 'Açúcar', 'CC=F':'Cacau', 
                                                                    'ZS=F': 'Soja', 'ZC=F':'Milho', 'LE=F':'Gado', 'KE=F':'Trigo'}))
#       tirando a hora '00:00:00' da coluna 'Date'
r_pd_commodities_tudo.index=r_pd_commodities_tudo.index.date

tab1, tab2, tab3, tab4 = st.tabs(["📈 Gráfico Geral", "🗓️ Report Semana", " 🙅‍♂️ Correlação Geral", "✅ Correlação Selecionada"])

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
    st.header("REPORT SEMANAL")
    tickers=yf.Tickers(lista_commodities)
    tickers_hist = tickers.history(period='max', start='2023-06-05', end='2023-06-12', interval='1wk')
    tickers_hist.stack(level=1).rename_axis(['Date', 'Ticker']).reset_index(level=1)
    tickers_hist.index=tickers_hist.index.date
    tickers_hist

    # df_comm_open = pd.pivot_table(tickers, index='Ticker', values='open', aggfunc='first')
    # df_comm_high = pd.pivot_table(tickers, index='Ticker', values='High', aggfunc='max')
    # df_comm_low = pd.pivot_table(tickers, index='Ticker', values='Low', aggfunc='min')
    # df_comm_close = pd.pivot_table(tickers, index='Ticker', values='Close', aggfunc='last')
    # df_comm_results = pd.concat([df_comm_open, df_comm_high, df_comm_low, df_comm_close], axis=1)
    # df_comm_results['Resultado_%'] = (df_comm_results.Close - df_comm_results.Open)/df_comm_results.Open*100
    # df_comm_results.head(10)
        
with tab3:
    st.header("CORRELAÇÃO")

    #       mostrando o dataframe da correlação
    st.dataframe(r_pd_commodities_tudo.corr())

    with st.expander("Ver explicação"):
        st.write("O DataFrame acima mostra a correlação das :blue[COMMODITIES].")

with tab4:
    st.header("CORRELAÇÃO SELECIONADA")
    st.write("Selecione pelo menos 2 :blue[COMMODITIES] para correlação!")
    #   adicionando espaço vazio
    st.text("")
    
    r_pd_commodities_tudo.index.date=r_pd_commodities_tudo.index
    todas_colunas=r_pd_commodities_tudo.columns.tolist()
    colunas_selecionadas=st.multiselect("", options=todas_colunas)
    #st.write("Você selecionou: ", colunas_selecionadas)

    if colunas_selecionadas:
        colunas_selecionadas_df=yf.download(todas_colunas, start=data_inicio, end=data_fim)['Adj Close']
        r_pd_colunas_selecionadas=pd.DataFrame(colunas_selecionadas_df.rename(columns={'CL=F':'Petroleo Cru', 'GC=F':'Ouro', 'HG=F':'Cobre', 'KC=F':'Café', 'NG=F':'Gás natural', 
                                                                    'PL=F':'Platina', 'SI=F':'Prata', 'CT=F':'Algodão', 'SB=F': 'Açúcar', 'CC=F':'Cacau', 
                                                                    'ZS=F': 'Soja', 'ZC=F':'Milho', 'LE=F':'Gado', 'KE=F':'Trigo'}))
        st.dataframe(r_pd_colunas_selecionadas.corr())
    else:
        st.warning("INVÁLIDO!")

