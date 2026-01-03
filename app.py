import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Calculadora Costura Pro", page_icon="🧵")

# --- MEMORIA (Estado de la sesión) ---
if 'galeria' not in st.session_state:
    st.session_state.galeria = []

# --- TÍTULO ---
st.title("🧵 Calculadora de Metraje")
st.markdown("Herramienta profesional para camisas de caballero.")

# --- PESTAÑAS ---
tab1, tab2 = st.tabs(["🧮 CALCULADORA", "📂 GALERÍA DE PROYECTOS"])

# === PESTAÑA 1: CALCULADORA ===
with tab1:
    st.subheader("Ingresa las medidas")
    
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre del Cliente", placeholder="Ej. Juan Pérez")
        pecho = st.number_input("Pecho (cm)", min_value=50, max_value=180, value=100)
    with col2:
        largo_c = st.number_input("Largo Camisa (cm)", value=75)
        largo_m = st.number_input("Largo Manga (cm)", value=65)
    
    ancho_tela = st.select_slider("Ancho de la Tela (cm)", options=[90, 110, 140, 150, 160], value=150)

    if st.button("CALCULAR METRAJE ✂️"):
        # CÁLCULOS
        ancho_pieza = (pecho / 4) + 6 + 5
        ancho_total_cuerpo = (ancho_pieza * 4) + 8 
        total_metros = (largo_c + largo_m + 5 + 10 + 10) / 100
        cabe_en_tela = ancho_total_cuerpo <= ancho_tela
        
        # RESULTADOS
        st.divider()
        st.markdown(f"### 🛍️ Resultado para: **{nombre}**")
        st.metric(label="Metraje a Comprar", value=f"{total_metros} m")
        
        if not cabe_en_tela:
            st.error(f"⚠️ El cuerpo ({ancho_total_cuerpo}cm) es más ancho que la tela ({ancho_tela}cm).")
            st.info("💡 Compra el DOBLE de tela.")
            nota = "⚠️ Doble Tela"
        else:
            st.success("✅ El patrón cabe perfectamente.")
            nota = "✅ Estándar"

        # GUARDAR
        nuevo = {
            "Fecha": datetime.now().strftime("%d/%m/%Y"),
            "Cliente": nombre if nombre else "Anónimo",
            "Medidas": f"{pecho}/{largo_c}/{largo_m}",
            "Metraje": f"{total_metros} m",
            "Nota": nota
        }
        st.session_state.galeria.append(nuevo)
        st.toast("Guardado en Galería", icon="💾")

# === PESTAÑA 2: GALERÍA ===
with tab2:
    st.header("📂 Historial")
    if len(st.session_state.galeria) > 0:
        df = pd.DataFrame(st.session_state.galeria)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aún no hay proyectos guardados.")
