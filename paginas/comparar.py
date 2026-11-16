import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Comparar horarios")

if st.session_state.df is None:
    st.info("Ve a la página 'Explorar los datos' y carga el archivo bicicletas_listas.csv para comenzar.")
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

if len(df) == 0:
    st.warning("No hay registros que cumplan los filtros actuales.")
    st.stop()

# Agrupar por hora y calcular promedio (R6)
promedios_hora = df.groupby("hora")["alquileres"].mean().reset_index()
promedios_hora.columns = ["Hora", "Promedio"]

# --- R6: Selector de color y gráfico de barras ---
color_barras = st.color_picker("Color de las barras", value="#197A8D")

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(promedios_hora["Hora"], promedios_hora["Promedio"], color=color_barras)
ax.set_xlabel("Hora del día")
ax.set_ylabel("Alquileres por hora observada")
ax.set_xticks(range(0, 24, 2))
ax.grid(axis="y", linestyle="--", alpha=0.4)
st.pyplot(fig)

# --- R6: Casilla para mostrar u ocultar tabla ---
if st.checkbox("Mostrar tabla de promedios"):
    tabla_prom = promedios_hora.copy()
    tabla_prom["Promedio"] = tabla_prom["Promedio"].round(2)
    st.dataframe(tabla_prom, use_container_width=True, hide_index=True)

st.divider()

# --- R7: Límite de alquileres por hora ---
limite = st.number_input("Límite de alquileres por hora", min_value=0, value=250, step=10)

superan = promedios_hora[promedios_hora["Promedio"] > limite]
cantidad_superan = len(superan)
total_horas = len(promedios_hora)

st.metric("Horarios con promedio mayor que el límite", f"{cantidad_superan}/{total_horas}")

if cantidad_superan > 0:
    lista_horas = [f"{int(h):02d}:00" for h in superan["Hora"]]
    st.write(f"**Horarios:** {', '.join(lista_horas)}.")
else:
    st.write("**Horarios:** Ninguno.")
