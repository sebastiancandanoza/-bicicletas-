import streamlit as st

st.set_page_config(page_title="BiciDatos", layout="wide")

if "df" not in st.session_state:
    st.session_state.df = None

with st.sidebar:
    st.title("BiciDatos")

pg_explorar = st.Page("paginas/explorar.py", title="Explorar los datos", default=True)
pg_comparar = st.Page("paginas/comparar.py", title="Comparar horarios")

navegacion = st.navigation([pg_explorar, pg_comparar])

with st.sidebar:
    st.divider()
    st.selectbox(
        "Tipo de usuario",
        options=["Todos", "Ocasionales", "Registrados"],
        key="filtro_usuario"
    )
    st.radio(
        "Tipo de día",
        options=["Todos", "Laborable", "No laborable"],
        key="filtro_dia"
    )
    st.slider(
        "Horas del día",
        min_value=0,
        max_value=23,
        value=(0, 23),
        key="filtro_horas"
    )

navegacion.run()
