
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


def main():
    '''
    Función principal de la interfaz
    '''

    st.set_page_config(page_title="Formulario", page_icon='📂', layout="wide")


    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
        )

    authenticator.login(location='main')


    if st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')

    if st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

    if st.session_state["authentication_status"]:
        usuario = st.session_state["name"]
    
        # configuramos algunos elementos de la página
        

        selected = option_menu(menu_title=None,
                                options=["Formulario", "Info"],
                                default_index=0,
                                icons=["house","clipboard-data"],
                                orientation="horizontal")

        if selected == "Formulario":
            st.write('Formulario aquí')


        if selected == "Info":
            st.write('Gráficas y tablas aquí')
if __name__ == "__main__":
    main()