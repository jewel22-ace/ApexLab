import streamlit as st
from streamlit_ace import st_ace
from streamlit_ace import st_ace, KEYBINDINGS, LANGUAGES, THEMES
import subprocess
import streamlit_authenticator as stauth
import yaml
from yaml import SafeLoader
import base64
import json
import requests



st.set_page_config(page_title="Apex Labs", page_icon="assest/icon.png", layout="wide", initial_sidebar_state="auto", menu_items=None)
col1, mid, col2 = st.columns([1,1,20])
with col1:
    st.image('assest/icon.png', width=70)
with col2:
    st.title('Apex Collab')

def encode(data):
    try:
        # Standard Base64 Encoding
        encodedBytes = base64.b64encode(data.encode("utf-8"))
        return str(encodedBytes, "utf-8")
    except:
        return ""

def decode(data):
    try:
        message_bytes = base64.b64decode(data)
        return message_bytes.decode('utf-8')
    except:
        return ""

def create_submission(code,lang_code=71,U_input=''):

    url = "https://judge0-ce.p.rapidapi.com/submissions"

    querystring = {"base64_encoded":"true","fields":"*"}

    payload = {
        "language_id": lang_code,
        "source_code": code,
        "stdin": U_input
    }
    headers = {
        "content-type": "application/json",
        "Content-Type": "application/json",
        "X-RapidAPI-Key": "549dda3c21msh54ce2b9ce00e877p138264jsn0fa210f13874",
        "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers, params=querystring)
    
    try :
    
        j_o=json.loads(response.text)['token']

    except Exception as e :

        j_o=''

    return response,j_o

def get_submission(token):

    url = "https://judge0-ce.p.rapidapi.com/submissions/"+str(token)

    querystring = {"base64_encoded":"true","fields":"*"}

    headers = {
        "X-RapidAPI-Key": "549dda3c21msh54ce2b9ce00e877p138264jsn0fa210f13874",
        "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    
    return response

def handle_get_submission_response(response):

    response=response.json()
    if str(response['stderr']) != "None" :

        error='Exit Code : '+str(response['exit_code'])+'\n'+'Error : '+decode(response['stderr'])+'\n'+'Satus : '+str(response['status'])+'\n'+'Message : '+decode(response['message'])
        
        return error

    else :

        output='Exit Code : '+str(response['exit_code'])+'\n'+'Status : '+str(response['status'])+'\n'+'---------------'+'\n'+'Output : '+decode(str(response['stdout']))
    
        return output




if st.session_state["authentication_status"]:
    
    with st.container():
        col1,col2 =st.columns([4,2])
        with col1 :
            content = st_ace(
                placeholder="Write your code here",
                language="python",
                theme="twilight",
                keybinding="vscode",
                font_size=15,
                tab_size=4,
                show_gutter=True,
                show_print_margin=True,
                wrap=True,
                auto_update=False,
                readonly=False,
                min_lines=30,
                key="ace",
            )

        with col2 :
            lang=st.selectbox('language',('Python','C'))
            st.subheader('Input')
            U_input=st.text_area('Uinput',placeholder="Input",height=150,label_visibility="collapsed")

        #content

        
   
        #if content[-2:] == './':
        #    prompt=content[int(content.index('/.'))+2:-2]
        #    st.write(prompt)
        if content :

            code=encode(content)
            
            response,token=create_submission(code,U_input=encode(U_input))
            #st.write(response.status_code)
            #st.write(response.json())
            #st.write(token)

            if token != '' :

                response=get_submission(token)
                #st.write(response.status_code)
                #st.write(response.json())
                #st.write(decode(c_output))
                output=handle_get_submission_response(response)

                col2.subheader('Output')
                col2.text_area('Output',label_visibility="collapsed",value=output,height=200)

            else:

                st.error(response.text)
            


elif st.session_state["authentication_status"] is None:
    st.info('Login to access')

elif st.session_state["authentication_status"] is False:
    st.info('Login to access')

