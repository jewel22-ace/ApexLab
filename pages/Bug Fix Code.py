import streamlit as st
import os
import openai
from streamlit_ace import st_ace
from streamlit_ace import st_ace, KEYBINDINGS, LANGUAGES, THEMES



os.environ['OPENAI_API_KEY'] = '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'

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Apex Labs", page_icon="assest/icon.png", layout="wide", initial_sidebar_state="auto", menu_items=None)
col1, mid, col2 = st.columns([1,1,20])
with col1:
    st.image('assest/icon.png', width=70)
with col2:
    st.title('Apex Fix')

if st.session_state["authentication_status"]:
    lang=st.selectbox('Select Language',('Python','Java'))
    st.subheader('Enter Code')
    prompt = st_ace(
            placeholder="Write your code here",
            language="python",
            theme="twilight",
            keybinding="vscode",
            font_size=15,
            tab_size=4,
            show_gutter=True,
            show_print_margin=False,
            wrap=True,
            auto_update=True,
            readonly=False,
            min_lines=30,
            key="ace",
        )

    button_check = st.button("Fix Code")
    
    prompt_helper="Fix bugs in the below function \n ### Buggy Python \n"
    if button_check and  prompt != '':
        #st.write(prompt)
        response = openai.Completion.create(
              model="code-davinci-002",
              prompt=prompt_helper+prompt,
              temperature=0,
              max_tokens=182,
              top_p=1,
              frequency_penalty=0,
              presence_penalty=0,
              
            )

        output=(response['choices'][0]["text"])
        print(output)
        st.subheader('Output')
        st.text_area('',height=200,value=output.strip())
    

elif st.session_state["authentication_status"] is None:
    st.info('Login to access')

elif st.session_state["authentication_status"] is False:
    st.info('Login to access')

