import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Explorar los datos")

# --- R1: Cargar los datos ---
archivo = st.file_uploader("Selecciona bicicletas_listas.csv", type=["csv"])

if st.button("Cargar datos", type="primary"):
    if archivo is not None:
        df_cargado = pd.read_csv(
            archivo,
            sep=",",
            encoding="utf-8-sig",
            parse_dates=["fecha"]
        )
        st.session_state.df = df_cargado
        st.success(f"{len(df_cargado):,} registros cargados.")
    else:
        st.warning("Por favor, selecciona primero el archivo bicicletas_listas.csv.")

if st.session_state.df is None:
    st.info("Sube el archivo bicicletas_listas.csv y presiona 'Cargar datos' para comenzar.")
    st.stop()

# --- R3: Aplicar filtros compartidos ---
df = st.session_state.df.copy()
usuario = st.session_state.filtro_usuario
if usuario == "Todos":
    df["alquileres"] = df["alquileres_total"]
elif usuario == "Ocasionales":
    df["alquileres"] = df["alquileres_ocasionales"]
else:
    df["alquileres"] = df["alquileres_registrados"]

if st.session_state.filtro_dia != "Todos":
    df = df[df["tipo_dia"] == st.session_state.filtro_dia]

h_min, h_max = st.session_state.filtro_horas
df = df[(df["hora"] >= h_min) & (df["hora"] <= h_max)]

# --- R4: Indicadores ---
col1, col2 = st.columns(2)
total_alq = int(df["alquileres"].sum())
prom_hora = df["alquileres"].mean() if len(df) > 0 else 0.0

col1.metric("Total de alquileres", f"{total_alq:,}".replace(",", "."))
col2.metric("Promedio por hora observada", f"{prom_hora:,.1f}".replace(".", ","))

# --- R2: Dos pestañas ---
tab_grafico, tab_datos = st.tabs(["Gráfico diario", "Datos"])

# --- R4: Gráfico diario ---
with tab_grafico:
    if len(df) > 0:
        diario = df.groupby("fecha")["alquileres"].sum()
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(diario.index, diario.values, color="#197A8D")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Alquileres por día")
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        st.pyplot(fig)
    else:
        st.warning("No hay datos para los filtros seleccionados.")

# --- R5: Tabla y descarga ---
with tab_datos:
    df_mostrar = df.copy()
    df_mostrar["fecha"] = df_mostrar["fecha"].dt.strftime("%Y-%m-%d")
    st.dataframe(df_mostrar, use_container_width=True)
    
    csv_bytes = df_mostrar.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="Descargar datos filtrados",
        data=csv_bytes,
        file_name="bicicletas_filtradas.csv",
        mime="text/csv"
    )
    
    st.caption("Fanaee-T, H. (2013). Bike Sharing [Conjunto de datos]. UCI Machine Learning Repository. https://doi.org/10.24432/C5W894. Licencia CC BY 4.0.")
    st.link_button(
        label="Consultar la fuente en UCI",
        url="https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset"
    )
