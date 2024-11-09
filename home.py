import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from io import BytesIO

# Inicializar una lista para almacenar las respuestas globalmente
responses = []

def download_excel(dataframe):
    """
    Función para generar un archivo Excel descargable.
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        dataframe.to_excel(writer, index=False, sheet_name='Respuestas')
    processed_data = output.getvalue()
    return processed_data

def formulario():
    """
    Función para mostrar y procesar el formulario.
    """
    st.header("Formulario de Registro")

    # Crear un formulario usando `st.form`
    with st.form("user_form"):
        # Campos del formulario
        name = st.text_input("Nombre")
        role = st.text_input("Rol")
        tools = st.multiselect(
            "Herramientas usadas",
            ["Python", "R", "SQL", "Excel", "Power BI", "Tableau", "Snowflake", "dbt"]
        )

        # Botón para enviar el formulario
        submit = st.form_submit_button("Enviar")

        # Procesar el formulario al hacer clic en "Enviar"
        if submit:
            if name and role and tools:
                response = {"Nombre": name, "Rol": role, "Herramientas": ", ".join(tools)}
                responses.append(response)
                st.success("¡Datos guardados exitosamente!")
            else:
                st.error("Por favor, llena todos los campos antes de enviar.")

    # Mostrar las respuestas recopiladas en una tabla
    if responses:
        df = pd.DataFrame(responses)
        st.subheader("Respuestas recopiladas")
        st.dataframe(df)

        # Generar archivo Excel descargable
        excel_data = download_excel(df)
        st.download_button(
            label="Descargar Excel",
            data=excel_data,
            file_name="respuestas_formulario.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


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

    # Realizar el login
    authenticator.login(location='main')

    # Comprobar el estado de autenticación
    if st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
        return

    if st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
        return

    if st.session_state["authentication_status"]:
        usuario = st.session_state["name"]

        # Configuración del menú lateral
        selected = option_menu(
            menu_title=None,
            options=["Formulario", "Info"],
            default_index=0,
            icons=["house", "clipboard-data"],
            orientation="horizontal"
        )

        # Opción del menú: Formulario
        if selected == "Formulario":
            formulario()

        # Opción del menú: Info
        if selected == "Info":
            st.header("Gráficas y tablas aquí")
            st.write("Esta sección puede incluir gráficos, tablas o cualquier otra información adicional.")

if __name__ == "__main__":
    main()
