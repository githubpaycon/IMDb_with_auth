# import streamlit as st
from src.base.base import *
from src.app.app import executar_bot
from src.database.database import faz_dataframe
import plotly.graph_objects as go
import plotly.express as px
import plotly.express as px
import datetime
import pytz
import streamlit_authenticator as stauth
import database as db
import time
    
st.set_page_config(initial_sidebar_state="collapsed", page_title='IMDb - Data Analysis', page_icon='🎥', menu_items={
        'Get Help': 'https://api.whatsapp.com/send?phone=5511985640273',
        'Report a bug': "https://api.whatsapp.com/send?phone=5511985640273",
        'About': "### Trabalhando por um futuro melhor. Com muito Amor, Inteligência e Vontade!"
    },
    layout="wide") # or centered

VERSION_APP = '2.0.0'


# --- CONFIGURAÇÕES ---
bar = st.sidebar
bar.title('Configurações')
page = bar.selectbox('Configurações básicas', ['Home', 'Esqueci a senha...', 'Fazer Logout/Login'])
bar.markdown('Escolha Home para')
if page == 'Esqueci a senha...':
    st.warning('Entre em contato com o nosso time, para que possamos trocar ou recuperar a sua senha.')



# --- AUTENTICAÇÃO DO USUÁRIO ---
users = db.fetch_all_users()
usernames = [user["key"] for user in users]
names = [user["name"] for user in users]
hashed_passwds = [user["password"] for user in users]
try:
    credentials = {
        "usernames":{
            usernames[0]:{
                "name":names[0],
                "password":hashed_passwds[0]
                },

            }
        }
except Exception as e:
    st.error('OCORREU UM ERRO AO RECUPERAR OS CREDENCIAIS, O DESENVOLVEDOR NÃO ADICIONOU ALGUM, ENTRE EM CONTATO COM ELE', icon='🤔')
    st.stop()
#                                                                       # coockie name, ass.do coockie, tempo_de_expiracao_do_coockie
authenticator = stauth.Authenticate(credentials, 'sales', 'abcdef', cookie_expiry_days=30)

name, authentication_status, username = authenticator.login('Login', 'main')


if authentication_status:  # se as credenciais baterem...
    if page == 'Fazer Logout/Login':
        authenticator.logout('Logout', 'main')
    if page == 'Home':
        with st.expander('Boas vindas...'):
            st.markdown(f'### Bem vindo: *{name}* <br>😀', True)
            st.markdown('Ficamos exultantes por você estar utilizando o nosso **Data App**!')
            st.markdown('Nessa plataforma podemos fazer coisas inimaginaveis, como por exemplo... <br>**Soltar balões**...', True)
            baloes = st.button('**Soltar balões...**')
            if baloes: st.balloons()
            st.markdown('**Ou neve...**', True)
            baloes = st.button('Soltar neve...')
            if baloes: st.snow()
            st.markdown('Também podemos prever quando algo vai acabar...', True)
            barra = st.button('Barra...')
            if barra:
                my_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.001)
                    my_bar.progress(percent_complete + 1)
            st.markdown('Estamos sempre aprendendo e descobrindo novos caminhos para trazer comodidade e rapidez para todos, eliminar trabalhos repetitivos e deixar que você tome um café, enquando o nosso bot faz o trabalho para você! 😅', True)
            
            

        st.markdown('# Extração de Filmes do <a href="https://www.imdb.com/chart/top/?ref_=nv_mv_250">IMDb</a>', True)
        st.subheader('👇 Execute o robô...')
        btn_executar = st.button('Executar Extração')
        if btn_executar:
            with st.expander('Execução do robô', True):
                executar_bot()
                df = faz_dataframe()
                my_date = datetime.datetime.now(pytz.timezone('America/Sao_Paulo'))
                df.to_excel('base.xlsx', f'{my_date.strftime("%d.%m.%Y %H_%M_%S")}')
            st.success('Robô Finalizado!')

        with st.expander('Gráficos...', True):
            try:
                df = pd.read_excel('base.xlsx', 0)
                data_da_atualizacao = pd.ExcelFile("base.xlsx").sheet_names[0]
                data_da_atualizacao = data_da_atualizacao.replace('.', '/').replace('_', ':')
                st.markdown(f'##### Data da Última Execução: <span style="color:blue">*{data_da_atualizacao}*</span>', True)
                del df['Unnamed: 0']
                view = st.selectbox('Escolha o tipo de visualização', [
                    'Tabela DataFrame',
                    'Tabela Plotly',
                    'Tabela Fixa',
                    'Gráfico de Barras | Streamlit',
                    'Grático de Barras | Plotly',
                    'Grafico de "Pizza" | Plotly',
                    'Gráfico Reluzente | Plotly'
                    ])

                if view == 'Gráfico de Barras | Streamlit':
                    x = st.selectbox('Eixo: X', list(df.columns), index=2) # index é o default
                    y = st.selectbox('Eixo: Y', list(df.columns), index=1)

                    st.bar_chart(df, x=x, y=y)
                if view == 'Grafico de "Pizza" | Plotly':
                    values = st.selectbox('Valores', list(df.columns), index=2) # index é o default
                    names = st.selectbox('Nomes', list(df.columns), index=1)
                    tamanho_hole = st.slider('Tamanho do Furo', min_value=0.001, max_value=1.0)
                    filmes = st.multiselect('Filmes', list(df['NOME DO FILME']), key='2', default=list(df['NOME DO FILME'])[10])
                    if len(filmes) == 0:
                        df = pd.read_excel('base.xlsx', 0)
                    else:
                        df = df.loc[df['NOME DO FILME'].isin(filmes)]

                    
                    fig = px.pie(df, values=values, names=names, hole=tamanho_hole)            
                    st.plotly_chart(fig, True)
                if view == 'Tabela DataFrame':
                    st.dataframe(df)
                if view == 'Grático de Barras | Plotly':
                    x = st.selectbox('Eixo: X', list(df.columns), index=2) # index é o default
                    y = st.selectbox('Eixo: Y', list(df.columns), index=1)
                    largura_grafico = st.slider('Largura do Gráfico', min_value=800, max_value=2000)
                    altura_grafico = st.slider('Altura do Gráfico', min_value=300, max_value=2000)
                    filmes = st.multiselect('Filmes', list(df['NOME DO FILME']))
                    if len(filmes) == 0:
                        df = pd.read_excel('base.xlsx', 0)
                    else:
                        df = df.loc[df['NOME DO FILME'].isin(filmes)]
                    fig = px.bar(df, x=x, y=y, title="Filme por ano", width=largura_grafico, height=altura_grafico)
                    st.plotly_chart(fig)

                if view == 'Tabela Fixa':
                    st.table(df)
                if view == 'Tabela Plotly':            
                    fig = go.Figure(data=[go.Table(
                                    header=dict(values=list(df.columns),
                                                line_color='darkslategray',
                                                fill_color='paleturquoise',
                                                align='left'),
                                    cells=dict(values=df.transpose().values.tolist(),
                                            fill_color='lavender',
                                            align='left'))
                                ])
                    fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
                    st.plotly_chart(fig)
                if view == 'Gráfico Reluzente | Plotly':
                    formato_de_apresentacao_dos_filmes = st.radio("Escolher filme por:", ('Nomes', 'Quantidade de Filmes'))
                    if formato_de_apresentacao_dos_filmes == 'Nomes':
                        filmes = st.multiselect('Filmes', list(df['NOME DO FILME']), default=list(df['NOME DO FILME'])[0:20])
                        if len(filmes) == 0:
                            df = df.loc[df['NOME DO FILME'].isin(df['NOME DO FILME'].to_list())]
                        else:
                            df = df.loc[df['NOME DO FILME'].isin(filmes)]
                    if formato_de_apresentacao_dos_filmes == 'Quantidade de Filmes':
                        qtd_files = st.slider('Escolha quantos filmes você quer filtrar...', max_value=len(list(df['NOME DO FILME'])))
                        filmes = st.multiselect('Filmes', list(df['NOME DO FILME']), default=list(df['NOME DO FILME'])[0:qtd_files])
                        if len(filmes) == 0:
                            df = df.loc[df['NOME DO FILME'].isin(df['NOME DO FILME'].to_list())]
                        else:
                            df = df.loc[df['NOME DO FILME'].isin(filmes)]

                    path = st.multiselect('Caminhos', list(df.columns), default=[df.columns[2], df.columns[1]]) # index é o default
                    print(path)
                    # if len(path) == 0:
                    #     df = pd.read_excel('base.xlsx', 0)
                    # else:
                    #     df = df.loc[df['NOME DO FILME'].isin(filmes)]
                    values = st.selectbox('Valores', list(df.columns), index=2)
                    print(values)

                    try:
                        fig = px.sunburst(df, path=path, values=values)
                        st.plotly_chart(fig)
                    except Exception:
                        st.error(f'Nao é possível fazer o gráfico com o valor "{values}"')
            except FileNotFoundError:
                st.warning('O robô ainda não foi executado, não existe nenhuma base.', icon='🤖')
elif authentication_status == False:
    st.error('Usuário ou Senha Incorreto!', icon='🙁')
elif authentication_status == None:
    st.warning('Por favor, insira seu usuário e senha...')


# parsed_toml = toml.load('autenticator.toml', )
# print(parsed_toml)
# autenticado = False
# if parsed_toml['autenticator']['isautenticator'] == False:
#     st.title('Autenticação')
#     user_inp = st.text_input('Usuário:')
#     passwd_inp = st.text_input('Senha:', type='password')
#     if st.button('Autenticar...'):
#         if user_inp == 'user' and passwd_inp == 'senha':
#             autenticado = True
# else:
# container = st.container()



st.markdown('</br></br></br></br>', True)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('###### <a href="https://paycon.com.br/">Paycon Payroll Consulting Labor & Human Resources</a>', True)
    st.markdown('###### Gabriel Lopes - Junior Analyst in Python')
    st.markdown('</br></br></br></br>', True)
    st.markdown(f'##### V{VERSION_APP}')
    st.text(' ')
with c3:
    with open("payconautomacoes.png", "rb") as e:
        st.image(e.read(), width=150, clamp=True)
