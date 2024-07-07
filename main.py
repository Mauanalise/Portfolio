import streamlit as st
from streamlit import session_state as ss
from streamlit_cookies_controller import CookieController
import time

# Configurações do Cookie
cookie_name = 'my_cookie_name'  # Substitua pelo nome do seu cookie
controller = CookieController(key='cookies')

# Dados de usuários para autenticação
USERS = {
    'john': {'username': 'john', 'password': 'jjj'},
    'peter': {'username': 'peter', 'password': 'ppp'}
}

# Função de autenticação
def authenticate():
    usern = ss.username
    passw = ss.password

    user_info = USERS.get(usern, {})
    
    if len(user_info):
        user_password = USERS.get(usern, {}).get('password', '')

        if user_password == passw:
            # Salvar nos cookies
            controller.set(f'{cookie_name}_username', ss.username, max_age=8*60*60)
            controller.set(f'{cookie_name}_password', ss.password, max_age=8*60*60)
            ss.login_ok = True

    if not ss.login_ok:
        st.error('Usuário ou senha incorretos.')

# Verificação inicial de cookies
if 'login_ok' not in ss:
    # Verificar o conteúdo dos cookies
    cookies = controller.getAll()
    time.sleep(1)

    # Obter nome de usuário e senha dos cookies, se existirem
    cookie_username = controller.get(f'{cookie_name}_username')
    cookie_password = controller.get(f'{cookie_name}_password')

    if cookie_username and cookie_password:
        ss.login_ok = True
        ss.username = cookie_username
        ss.password = cookie_password
        st.success(f'Bem-vindo de volta, {ss.username}!')
    else:
        ss.login_ok = False

# Interface de login
if not ss.get('login_ok', False):
    st.title("Página de Login")
    ss.username = st.text_input("Nome de usuário")
    ss.password = st.text_input("Senha", type="password")

    if st.button("Login"):
        authenticate()
else:
    # Interface após login
    st.sidebar.title("Navegação")
    page = st.sidebar.radio("Ir para", ["Home", "Perfil", "Logout"])

    if page == "Home":
        st.title("Página Inicial")
        st.write(f"Bem-vindo, {ss.username}!")

    elif page == "Perfil":
        st.title("Perfil do Usuário")
        st.write(f"Nome de usuário: {ss.username}")

    elif page == "Logout":
        st.title("Logout")
        if st.button("Confirmar Logout"):
            # Limpar cookies e estado da sessão
            controller.delete(f'{cookie_name}_username')
            controller.delete(f'{cookie_name}_password')
            ss.clear()  # Limpar o estado da sessão
            st.experimental_rerun()
