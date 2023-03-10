import streamlit as st
from streamlit_ace import st_ace
from streamlit_ace import st_ace, KEYBINDINGS, LANGUAGES, THEMES
from pathlib import Path
import pickle
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
import yaml
from yaml import SafeLoader




st.set_page_config(page_title="Apex Labs", page_icon="assest/icon.png", layout="wide", initial_sidebar_state="auto", menu_items=None)
col1, mid, col2 = st.columns([1,1,20])
with col1:
    st.image('assest/icon.png', width=70)
with col2:
    st.title('Apex Labs')

st.write("Welcome to the world of Python programming! Whether you're a beginner or an experienced developer, our online code IDE makes it easy to write, test, and run Python code from anywhere. With powerful features, intuitive design, and robust security, our platform is perfect for coding enthusiasts, educators, and businesses alike.")

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
try :

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

except Exception as e :
    st.error(e)



if st.session_state["authentication_status"]:
    with st.sidebar:
        
        st.write(f'Welcome *{st.session_state["name"]}*')
        authenticator.logout('Logout', 'main')



elif st.session_state["authentication_status"] is False:
    tab1, tab2= st.tabs(["Login", "Register"])
    with tab1:
        name, authentication_status, username = authenticator.login('Login', 'main')
        if st.session_state["authentication_status"] is False:
            st.error('Username/password is incorrect')
        elif st.session_state["authentication_status"] is None:
            st.warning('Please enter your username and password')
    with tab2:
        try:
            if authenticator.register_user('Register user', preauthorization=False):
                with open('config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
                st.success('User registered successfully')
        except Exception as e:
            st.error(e)

elif st.session_state["authentication_status"] is None:
    tab1, tab2= st.tabs(["Login", "Register"])
    with tab1:
        name, authentication_status, username = authenticator.login('Login', 'main')
        if st.session_state["authentication_status"] is False:
            st.error('Username/password is incorrect')
        elif st.session_state["authentication_status"] is None:
            st.warning('Please enter your username and password')
    with tab2:
        try:
            if authenticator.register_user('Register user', preauthorization=False):
                with open('config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
                st.success('User registered successfully. Login and Happy coding')
        except Exception as e:
            st.error(e)


