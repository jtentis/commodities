import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib
from datetime import date, timedelta
from PIL import Image
import time

st.set_page_config(
    page_title="Página inicial / Commodities",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.google.com'
    }
)

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)  

st.title("DASHBOARD DAS :orange[COMMODITIES]")

#       ordem das commodites no array: ouro, prata, platina, cobre, pretoleo cru, gas natural e café. 
lista_commodities = ['GC=F', 'SI=F', 'PL=F', 'HG=F', 'CL=F', 'NG=F', 'KC=F', 'SB=F', 'CT=F', 'CC=F', 'ZS=F', 'ZC=F', 'LE=F', 'KE=F']

image=Image.open("imagens/OBInvestLogo.png")

#       recebendo a data do input
with st.sidebar:
    st.sidebar.image(image)
    st.text("")
    st.title(':orange[FILTRO]')
    data_inicio=st.date_input("Escolha a data inicial:", datetime.date(2023, 1, 1))
    data_fim=st.date_input("Escolha a data final:", date.today())
    st.divider()
    st.title(':orange[HEATMAP]')
    heatmap_botao = st.radio("Selecione o modo:",('Ligado', 'Desligado'))
    st.divider()
    st.title(':orange[TABELA]')
    tabela_botao = st.radio("Selecione o tipo de tabela:",('Compacta', 'Grande'))
    # with st.container():
    #     st.write("")
    #     st.write("")
    #     st.write("")
    #     st.write("")
    #     st.write("")
    #     st.write("")
    #     st.write("")
    #     st.write("")
    #     st.write("")
    # # with st.spinner('Carregando...'):
    # #     time.sleep(2)

#       fazendo download dos valores via yfinance
commodities_tudo=yf.download(lista_commodities, start=data_inicio, end=data_fim)['Adj Close']
# commodities_report=yf.download(lista_commodities, period='1mo', interval='1wk', group_by='ticker')

tickers = yf.Tickers(lista_commodities)
week=data_fim-timedelta(days=8)
tickers_hist = tickers.history(start=week, end=data_fim, interval='1wk')

#       renomeando as commodities
r_pd_commodities_tudo=pd.DataFrame(commodities_tudo.rename(columns={'CL=F':'Petroleo Cru', 'GC=F':'Ouro', 'HG=F':'Cobre', 'KC=F':'Café', 'NG=F':'Gás natural', 
                                                                    'PL=F':'Platina', 'SI=F':'Prata', 'CT=F':'Algodão', 'SB=F': 'Açúcar', 'CC=F':'Cacau', 
                                                                    'ZS=F': 'Soja', 'ZC=F':'Milho', 'LE=F':'Gado', 'KE=F':'Trigo'}))
dif_percentual={'CL=F':'Petroleo Cru', 'GC=F':'Ouro', 'HG=F':'Cobre', 'KC=F':'Café', 'NG=F':'Gás natural', 
                'PL=F':'Platina', 'SI=F':'Prata', 'CT=F':'Algodão', 'SB=F': 'Açúcar', 'CC=F':'Cacau', 
                'ZS=F': 'Soja', 'ZC=F':'Milho', 'LE=F':'Gado', 'KE=F':'Trigo'}
r_tickers_hist=pd.DataFrame(tickers_hist.rename(columns={'CL=F':'Petroleo Cru', 'GC=F':'Ouro', 'HG=F':'Cobre', 'KC=F':'Café', 'NG=F':'Gás natural', 
                                                                    'PL=F':'Platina', 'SI=F':'Prata', 'CT=F':'Algodão', 'SB=F': 'Açúcar', 'CC=F':'Cacau', 
                                                                    'ZS=F': 'Soja', 'ZC=F':'Milho', 'LE=F':'Gado', 'KE=F':'Trigo'}))
#       tirando a hora '00:00:00' da coluna 'Date'
r_pd_commodities_tudo.index=r_pd_commodities_tudo.index.date
r_tickers_hist.index=r_tickers_hist.index.date

tab1, tab2, tab3, tab4 = st.tabs(["📈 Gráfico Geral", "🗓️ Report Semanal", " 🙅‍♂️ Correlação Geral", "✅ Correlação Selecionada"])

with tab1:
    st.header("TABELA")
    if tabela_botao == 'Grande':
        st.table(r_pd_commodities_tudo)
    else:
        st.dataframe(r_pd_commodities_tudo)

    st.divider()
    
    #       plotando
    st.header("GRÁFICO")
    st.line_chart(r_pd_commodities_tudo)
    #st.bar_chart(r_pd_commodities_tudo)

    with st.expander("Ver explicação"):
        st.write("O gráfico acima mostra a variação de preço (em :green[U$]), das :orange[COMMODITIES].")
    
    st.download_button("Baixar Tabela", 
                       r_pd_commodities_tudo.to_csv(),
                       file_name='commodities_dados.csv',
                       mime='text/csv')

with tab2:
    st.header("REPORT SEMANAL")
    st.write(week,'a', data_fim)
    st.write("")
    tickers_report=r_tickers_hist.stack(level=1).rename_axis(['Data', 'Tickers']).reset_index(level=1)
    report_semanal=tickers_report.drop(['Dividends','Volume','Stock Splits'], axis=1)
    report_semanal['Resultado']=(report_semanal['Close'] - report_semanal['Open'])/report_semanal['Open']*100
    report_semanal=report_semanal[['Tickers', 'Open', 'High', 'Low', 'Close', 'Resultado']]
    report_semanal.rename(columns={'Tickers':'Commodities'}, inplace=True)
    report_semanal=report_semanal.sort_values('Resultado', ascending=True)
    download_report=report_semanal
    if tabela_botao == 'Compacta':
        # cmap=plt.cm.get_cmap('RdYlGn')
        # st.dataframe(report_semanal.style.background_gradient(cmap=cmap,vmin=(-1),vmax=1, axis=None, subset='Resultado %'))
        # colors = dict(zip(report_semanal['Resultado'].unique(),
        #           (f'background-color: {c}' for c in matplotlib.colors.cnames.values())))
        # st.dataframe(report_semanal.style.applymap(colors.get, subset=['Resultado']))
        # st.dataframe(report_semanal.style.applymap(lambda x:"background-color: %s"%x, subset=['Resultado']))
        # color_green='green'
        # report_semanal['Resultado'].style.background_gradient(cmap=cmap,vmin=(-1),vmax=1, axis=1)
        st.dataframe(report_semanal)
    else:
        st.table(report_semanal)

    data = yf.download(list(dif_percentual.keys()), start=week, end=data_fim)['Close']

    weekly_returns = data.pct_change(periods=1) * 100

    sorted_returns = weekly_returns.iloc[-1].sort_values(ascending=False)

    sorted_indices = sorted_returns.index

    positive_returns = sorted_returns[sorted_returns >= 0]
    negative_returns = sorted_returns[sorted_returns < 0]

    fig, ax = plt.subplots(figsize=(5, 8))
    ax.barh([dif_percentual[idx] for idx in positive_returns.index], positive_returns, color='green')
    ax.barh([dif_percentual[idx] for idx in negative_returns.index], negative_returns, color='red')
    ax.axvline(x=0, color='black', linestyle='--')
    plt.xlabel('Variação Percetual')
    plt.ylabel('Commodities')
    fig.set_figwidth(15)
    # fig.set_figheight(30)
    # plt.title('Variação Percentual em Relação a Semana Acima')

    # Adiciona as porcentagens ao lado de cada barra
    for i, (index, value) in enumerate(zip(positive_returns.index, positive_returns)):
        ax.text(0, i, f'{value:.2f}%', ha='right', va='center', color='black', fontweight='bold')
        y = i
    for i, (index, value) in enumerate(zip(negative_returns.index, negative_returns)):
        ax.text(0, y+1+i, f'{value:.2f}%', ha='left', va='center', color='black', fontweight='bold')

    st.pyplot(plt.show())

    with st.expander("Ver explicação"):
        st.write("O gráfico acima mostra a variação percentual das :orange[COMMODITIES] de acordo com a semana escolhida.")
    
    st.download_button("Baixar Tabela", 
                       download_report.to_csv(),
                       file_name='commodities_table_report.csv',
                       mime='text/csv')
    
    # st.write("Selecione 1 :orange[COMMODITIE] para ver o Report Semanal!")
    # # options_key = "_".join(todas_colunas)
    # opcao_report = st.selectbox('',options=todas_colunas_report)
    # if opcao_report:
    #     report_semanal = r_pd_commodities_report[opcao_report]
    #     # result_report=yf.download(report_semanal, start=data_inicio, interval='1wk')
    #     # report_semanal=result_report.drop(['Adj Close','Volume'])
    #     # report_semanal['Resultado %']=(report_semanal['Close'] - report_semanal['Open'])/report_semanal['Open']*100
    #     st.dataframe(report_semanal)
    # else:  
    #     st.warning('INVÁLIDO!')

    # tickers=yf.Tickers(lista_commodities)
    # tickers_hist = tickers.history(period='max', start='2023-06-05', end='2023-06-12', interval='1wk')
    # tickers_hist.stack(level=1).rename_axis(['Date', 'Ticker']).reset_index(level=1)
    # tickers_hist.index=tickers_hist.index.date
    # tickers_hist

    # df_comm_open = pd.pivot_table(tickers, index='Ticker', values='open', aggfunc='first')
    # df_comm_high = pd.pivot_table(tickers, index='Ticker', values='High', aggfunc='max')
    # df_comm_low = pd.pivot_table(tickers, index='Ticker', values='Low', aggfunc='min')
    # df_comm_close = pd.pivot_table(tickers, index='Ticker', values='Close', aggfunc='last')
    # df_comm_results = pd.concat([df_comm_open, df_comm_high, df_comm_low, df_comm_close], axis=1)
    # df_comm_results['Resultado_%'] = (df_comm_results.Close - df_comm_results.Open)/df_comm_results.Open*100
    # df_comm_results.head(10)
        
with tab3:
    st.header("CORRELAÇÃO")

    #       mostrando o dataframe da correlação e colocando heatmap
    corr_commodities_tudo=r_pd_commodities_tudo.corr()
    download_all=r_pd_commodities_tudo.corr()
    if heatmap_botao == 'Ligado':
        if tabela_botao == 'Grande':
            cmap=plt.cm.get_cmap('RdYlGn')
            st.table(corr_commodities_tudo.style.background_gradient(cmap=cmap,vmin=(-1),vmax=1, axis=None))
        else:
            cmap=plt.cm.get_cmap('RdYlGn')
            st.dataframe(corr_commodities_tudo.style.background_gradient(cmap=cmap,vmin=(-1),vmax=1, axis=None))
    else:
        if tabela_botao == 'Compacta':
            st.dataframe(r_pd_commodities_tudo.corr())
        else:
            st.table(r_pd_commodities_tudo.corr())

    with st.expander("Ver explicação"):
        st.write("O DataFrame acima mostra a correlação das :orange[COMMODITIES].")

    st.download_button("Baixar Tabela", 
                       download_all.to_csv(),
                       file_name='commodities_table.csv',
                       mime='text/csv')

with tab4:
    st.header("CORRELAÇÃO SELECIONADA")
    st.write("Selecione pelo menos 2 :orange[COMMODITIES] para correlação!")
    st.text("")
    #   fazendo o multiselect
    todas_colunas = r_pd_commodities_tudo.columns.tolist()
    options_key = "_".join(todas_colunas)
    colunas_selecionadas = st.multiselect('', options=todas_colunas)
    
    if colunas_selecionadas:
        colunas_corr = r_pd_commodities_tudo[colunas_selecionadas]
        color_change_colunas_corr=colunas_corr.corr()
        if heatmap_botao == 'Ligado':
            if tabela_botao == 'Grande':
                cmap=plt.cm.get_cmap('RdYlGn')
                st.table(color_change_colunas_corr.style.background_gradient(cmap=cmap,vmin=(-1),vmax=1, axis=None))
            else:
                cmap=plt.cm.get_cmap('RdYlGn')
                st.dataframe(color_change_colunas_corr.style.background_gradient(cmap=cmap,vmin=(-1),vmax=1, axis=None))
        else:
            if tabela_botao == 'Compacta':
                st.dataframe(color_change_colunas_corr)
            else:
                st.table(color_change_colunas_corr)
    else:
        st.warning("INVÁLIDO!")
    
    download_selection=r_pd_commodities_tudo[colunas_selecionadas].corr()
    st.download_button("Baixar Tabela", 
                       download_selection.to_csv(),
                       file_name='commodities_table_selection.csv',
                       mime='text/csv')
