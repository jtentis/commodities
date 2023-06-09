import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta
from PIL import Image

#   configs da pagina
st.set_page_config(
    page_title="Página inicial / Commodities",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.google.com'
    }
)

#   comando para o programa ler o style.css
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)  

st.title("DASHBOARD DAS :orange[COMMODITIES]")

lista_commodities = ['GC=F', 'SI=F', 'PL=F', 'HG=F', 'CL=F', 'NG=F', 'KC=F', 'SB=F', 'CT=F', 'CC=F', 'ZS=F', 'ZC=F', 'LE=F', 'KE=F']
lista_ativos = ["^BVSP","GGBR4.SA", "CMIG4.SA", "PETR4.SA", "PETR3.SA", "VIVT3.SA", "VALE3.SA", "BBAS3.SA", "CPLE6.SA", "JBSS3.SA", 
                 "TRPL4.SA", "SANB11.SA", "BBSE3.SA", "EGIE3.SA", "B3SA3.SA", "TAEE11.SA", "ITSA4.SA", "VBBR3.SA", "GOAU4.SA", "CSNA3.SA", "CMIG3.SA", "CPFE3.SA",
                 "ABEV3.SA", "BBAS3.SA", "BBDC3.SA", "ELET3.SA", "ENGI11.SA", "RDOR3.SA", "RENT3.SA", "SUZB3.SA", "RAIZ4.SA", "JBSS3.SA", 
                 "MGLU3.SA", "AMER3.SA", "CRFB3.SA", "NTCO3.SA"]

#       função de download sendo armazenada no cache
@st.cache_data
def cache_comm(nome_modelo):
    commodities_tudo=yf.download(nome_modelo, start=data_inicio, end=data_fim)['Adj Close']
    return (commodities_tudo)

@st.cache_resource
def cache_ativos(nome_modelo):
    ativos_tudo=yf.download(nome_modelo, start=data_inicio, end=data_fim)['Adj Close']
    return (ativos_tudo)

@st.cache_resource
def cache_tickers(nome_modelo):
    tickers=yf.Tickers(nome_modelo)
    return (tickers)

@st.cache_resource
def cache_tickers_hist():
    download_hist = tickers.history(start=week, end=data_fim, interval='1wk')
    return (download_hist)

logo=Image.open("imagens/OBInvestLogo.png")

with st.sidebar:
    st.sidebar.image(logo)
    st.title(':orange[FILTRO]')
    semana=date.today()-timedelta(days=30)
    data_inicio=st.date_input("Escolha a data inicial:", semana)
    data_fim=st.date_input("Escolha a data final:")
    with st.expander("IMPORTANTE"):
        st.write("Caso queira mudar as datas, mude e depois clique no botão :orange[EXECUTAR CACHE] para salvar os dados no cache novamente!")
        if st.sidebar.button('Executar cache'):
            cache_comm.clear(), cache_ativos.clear(), cache_tickers.clear(), cache_tickers_hist.clear()
    st.divider()
    st.title(':orange[HEATMAP]')
    heatmap_botao = st.radio("Selecione o modo:",('Ligado', 'Desligado'))
    st.divider()
    st.title(':orange[TABELA]')
    tabela_botao = st.radio("Selecione o tipo de tabela:",('Compacta', 'Grande'))
    st.divider()
    st.write('')
    st.write('')
    st.markdown("[![Fonte](https://public.flourish.studio/uploads/4e293af7-8464-45d7-9428-a96963909e42.png)]"
                "(https://finance.yahoo.com/commodities/)")
        

commodities_tudo=cache_comm(lista_commodities)
ativos_tudo=cache_ativos(lista_ativos)
tickers = cache_tickers(lista_commodities)
week=data_fim-timedelta(days=1)
tickers_hist=cache_tickers_hist()

#       renomeando as commodities e passando para o pd
r_pd_commodities_tudo=pd.DataFrame(commodities_tudo.rename(columns={'CL=F':'Petroleo Cru', 'GC=F':'Ouro', 'HG=F':'Cobre', 'KC=F':'Café', 'NG=F':'Gás natural', 
                                                                    'PL=F':'Platina', 'SI=F':'Prata', 'CT=F':'Algodão', 'SB=F': 'Açúcar', 'CC=F':'Cacau', 
                                                                    'ZS=F': 'Soja', 'ZC=F':'Milho', 'LE=F':'Gado', 'KE=F':'Trigo'}))
dif_percentual={'CL=F':'Petroleo Cru', 'GC=F':'Ouro', 'HG=F':'Cobre', 'KC=F':'Café', 'NG=F':'Gás natural', 
                'PL=F':'Platina', 'SI=F':'Prata', 'CT=F':'Algodão', 'SB=F': 'Açúcar', 'CC=F':'Cacau', 
                'ZS=F': 'Soja', 'ZC=F':'Milho', 'LE=F':'Gado', 'KE=F':'Trigo'}
r_tickers_hist=pd.DataFrame(tickers_hist.rename(columns={'CL=F':'Petroleo Cru', 'GC=F':'Ouro', 'HG=F':'Cobre', 'KC=F':'Café', 'NG=F':'Gás natural', 
                                                                    'PL=F':'Platina', 'SI=F':'Prata', 'CT=F':'Algodão', 'SB=F': 'Açúcar', 'CC=F':'Cacau', 
                                                                    'ZS=F': 'Soja', 'ZC=F':'Milho', 'LE=F':'Gado', 'KE=F':'Trigo'}))
r_pd_ativos=pd.DataFrame(ativos_tudo)

#       tirar a hora '00:00:00' da coluna 'Date'
# r_pd_commodities_tudo.index=r_pd_commodities_tudo.index.date

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
    grafico_botao=st.radio("Selecione o modo do gráfico:",('Completo', 'Selecionado'))
    if grafico_botao == 'Completo':
        st.line_chart(r_pd_commodities_tudo)
    else:
        with st.form("grafico"):
            grafico_all=r_pd_commodities_tudo.columns.tolist()
            options_key = "_".join(grafico_all)
            selecao_grafico=st.multiselect('Selecione as commodities para plotar:', options=grafico_all)
            envido_grafico=st.form_submit_button("Executar")
        st.line_chart(r_pd_commodities_tudo[selecao_grafico])


    with st.expander("Ver explicação"):
        st.write("Acima, uma tabela e um gráfico que mostram a variação de preço (em :green[U$]), das :orange[COMMODITIES].")
    
    st.download_button("Baixar Tabela", 
                       r_pd_commodities_tudo.to_csv(),
                       file_name='commodities_dados.csv',
                       mime='text/csv')

with tab2:
    st.header("REPORT SEMANAL")
    week_texto=data_fim-timedelta(days=7)
    st.write(week_texto, 'a', data_fim)
    st.write("")
    tickers_report=r_tickers_hist.stack(level=1).rename_axis(['Data', 'Tickers']).reset_index(level=1)
    report_semanal=tickers_report.drop(['Dividends','Volume','Stock Splits'], axis=1)
    report_semanal['Resultado %']=(report_semanal['Close'] - report_semanal['Open'])/report_semanal['Open']*100
    report_semanal=report_semanal[['Tickers', 'Open', 'High', 'Low', 'Close', 'Resultado %']]
    report_semanal.rename(columns={'Tickers':'Commodities'}, inplace=True)
    report_semanal=report_semanal.sort_values('Resultado %', ascending=True)

    if tabela_botao == 'Compacta':
        st.dataframe(report_semanal)
        st.divider()
    else:
        st.table(report_semanal)
        st.divider()

    data = yf.download(list(dif_percentual.keys()), start=data_inicio, end=data_fim)['Close']

    weekly_returns = data.pct_change(periods=1, fill_method='ffill', axis=0) * 100
    sorted_returns = weekly_returns.iloc[-1].sort_values(ascending=False)
    sorted_indices = sorted_returns

    positive_returns = sorted_returns[sorted_returns >= 0]
    negative_returns = sorted_returns[sorted_returns < 0]

    fig, ax = plt.subplots(figsize=(5, 8))
    ax.barh([dif_percentual[idx] for idx in positive_returns.index], positive_returns, color='green')
    ax.barh([dif_percentual[idx] for idx in negative_returns.index], negative_returns, color='red')
    ax.axvline(x=0, color='white', linestyle='--')
    # plt.title('Diferença percentual em relação a semana anterior', color='w')
    # plt.xlabel('Variação Percetual')
    # plt.ylabel('Commodities')
    fig.set_figwidth(15)
    ax.set_facecolor('#0e1117')
    fig.set_facecolor('#0e1117')
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.spines['bottom'].set_color('#0e1117')
    ax.spines['top'].set_color('#0e1117')
    ax.spines['left'].set_color('#0e1117')
    ax.spines['right'].set_color('#0e1117')

    for i, (index, value) in enumerate(zip(positive_returns.index, positive_returns)):
        ax.text(0, i, f'{value:.2f}%', ha='right', va='center', color='white', fontweight='bold')
        y = i
    for i, (index, value) in enumerate(zip(negative_returns.index, negative_returns)):
        ax.text(0, y+1+i, f'{value:.2f}%', ha='left', va='center', color='white', fontweight='bold')

    st.subheader('Diferença percentual em relação a semana anterior')
    st.pyplot(plt.show())
    st.write('')
    st.write('')

    with st.expander("Ver explicação"):
        st.write("O gráfico acima mostra a variação percentual das :orange[COMMODITIES] de acordo com a semana escolhida, "
                 "que também pode ser visualizado pela tabela!")
    
    download_report=report_semanal
    st.download_button("Baixar Tabela", 
                        download_report.to_csv(),
                        file_name='commodities_table_report.csv',
                        mime='text/csv')
    
with tab3:
    st.header("CORRELAÇÃO")
    botao_corr=st.radio('Deseja ver com :blue[ATIVOS] juntos?',('Sim','Não'), index=1)
    resultado_juncao=pd.concat([r_pd_commodities_tudo, r_pd_ativos], axis='columns')
    #       mostrando o dataframe da correlação e colocando heatmap
    corr_commodities_tudo=r_pd_commodities_tudo.corr()
    if botao_corr == 'Sim':
        corr_commodities_tudo=resultado_juncao.corr()
    else:
        st.empty()
    if heatmap_botao == 'Ligado':
        if tabela_botao == 'Grande':
            cmap=plt.colormaps['RdYlGn']
            st.table(corr_commodities_tudo.style.background_gradient(cmap=cmap,vmin=(-1),vmax=1, axis=None))
        else:
            cmap=plt.colormaps['RdYlGn']
            st.dataframe(corr_commodities_tudo.style.background_gradient(cmap=cmap,vmin=(-1),vmax=1, axis=None))
    else:
        if tabela_botao == 'Compacta':
            st.dataframe(corr_commodities_tudo.corr())
        else:
            st.table(corr_commodities_tudo.corr())

    with st.expander("Ver explicação"):
        st.write("A tabela acima mostra a correlação das :orange[COMMODITIES] com :blue[ATIVOS], caso a opção tenha sido marcada.")

    download_all=corr_commodities_tudo
    st.download_button("Baixar Tabela", 
                       download_all.to_csv(),
                       file_name='commodities_table.csv',
                       mime='text/csv')

with tab4:
    st.header("CORRELAÇÃO SELECIONADA")
    st.write("Selecione :orange[COMMODITIES] e/ou :blue[ATIVOS] para a correlação! ")
    ativos_corr=st.radio("Deseja adicionar ativos para correlação?", ('Sim', 'Não'), index=1)
    #   fazendo o multiselect
    todas_colunas = r_pd_commodities_tudo.columns.tolist()
    # options_key = "_".join(todas_colunas)
    todas_colunas_ativos=r_pd_ativos.columns.tolist()
    # options_key = "_".join(todas_colunas_ativos)
    tudo=''
    enviado_ativo=''
    ativos_selecionados=''
    enviado_comm=''
    if ativos_corr == 'Não':
        with st.form("coluna_commodity"):
            comm_selecionadas = st.multiselect('Selecione as :orange[COMMODITIES]:', options=todas_colunas)
            enviado_comm=st.form_submit_button('Executar')
            tudo=comm_selecionadas
            download_selection=resultado_juncao[tudo].corr()
    else:
        with st.form("geral"):
            comm_selecionadas = st.multiselect('Selecione as :orange[COMMODITIES]:', options=todas_colunas)
            tudo=comm_selecionadas
            ativos_selecionados = st.multiselect('Selecione os :blue[ATIVOS]:', options=todas_colunas_ativos)
            tudo=(comm_selecionadas+ativos_selecionados)
            enviado_ativo=st.form_submit_button('Executar')
    download_selection=resultado_juncao[tudo].corr()

    if enviado_comm:
        colunas_corr = resultado_juncao[tudo]
        color_change_colunas_corr=colunas_corr.corr()
        download_selection=resultado_juncao[tudo].corr()
        if heatmap_botao == 'Ligado':
            if tabela_botao == 'Grande':
                cmap=plt.colormaps['RdYlGn']
                st.table(color_change_colunas_corr.style.background_gradient(cmap=cmap,vmin=(-1),vmax=1, axis=None))
            else:
                cmap=plt.colormaps['RdYlGn']
                st.dataframe(color_change_colunas_corr.style.background_gradient(cmap=cmap,vmin=(-1),vmax=1, axis=None))
        else:
            if tabela_botao == 'Compacta':
                st.dataframe(color_change_colunas_corr)
            else:
                st.table(color_change_colunas_corr)
    elif enviado_ativo:
        colunas_corr = resultado_juncao[tudo]
        color_change_colunas_corr=colunas_corr.corr()
        download_selection=resultado_juncao[tudo].corr()
        if heatmap_botao == 'Ligado':
            if tabela_botao == 'Grande':
                cmap=plt.colormaps['RdYlGn']
                st.table(color_change_colunas_corr.style.background_gradient(cmap=cmap,vmin=(-1),vmax=1, axis=None))
            else:
                cmap=plt.colormaps['RdYlGn']
                st.dataframe(color_change_colunas_corr.style.background_gradient(cmap=cmap,vmin=(-1),vmax=1, axis=None))
        else:
            if tabela_botao == 'Compacta':
                st.dataframe(color_change_colunas_corr)
            else:
                st.table(color_change_colunas_corr)
    else:
        st.empty()

    with st.expander("Ver explicação"):
        st.write("A tabela acima mostra a correlação das :orange[COMMODITIES] selecionadas entre si, ou com os :blue[ATIVOS] selecionados, caso a opção tenha sido marcada!")
    
    st.download_button("Baixar Tabela", 
                       download_selection.to_csv(),
                       file_name='commodities_table_selection.csv',
                       mime='text/csv')
