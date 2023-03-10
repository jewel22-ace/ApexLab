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
    st.title('Apex Translate')

st.subheader('Convert Code')
col_1,col_3=st.columns(2)
with col_1:
    from_=st.selectbox('From',('Python', 'Html', 'Java'))

with col_3:
    to=st.selectbox('To',('Python', 'Html', 'Java'))

if st.session_state["authentication_status"]:
    st.subheader('Enter Code')
    prompt = st_ace(
            placeholder="Write your code here",
            language="python",
            theme="twilight",
            keybinding="vscode",
            font_size=15,
            tab_size=4,
            show_gutter=True,
            show_print_margin=True,
            wrap=True,
            auto_update=True,
            readonly=False,
            min_lines=30,
            key="ace",
        )
    button_check = st.button("Translate")
    
    prompt_helper="Convert the code or function from "+str(from_)+" into "+str(to)+"\n"+str(from_)+"\n"
    if button_check and  prompt != '':
        #st.write(prompt)
        response = openai.Completion.create(
              model="code-davinci-002",
              prompt=prompt_helper+prompt,
              temperature=0,
              max_tokens=54,
              top_p=1,
              frequency_penalty=0,
              presence_penalty=0,
              
            )

        output=(response['choices'][0]["text"])
        
        st.subheader('Output')
        #st.text_area('',height=200,value=output.strip())
        st_ace(
            placeholder="Write your code here",
            language="python",
            theme="twilight",
            keybinding="vscode",
            font_size=15,
            value=output,
            tab_size=4,
            show_gutter=True,
            show_print_margin=True,
            wrap=True,
            auto_update=True,
            readonly=False,
            min_lines=30,
            key="ace_output",
        )
    

elif st.session_state["authentication_status"] is None:
    st.info('Login to access')

elif st.session_state["authentication_status"] is False:
    st.info('Login to access')

