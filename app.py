import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Calculadora Costura Pro", page_icon="🧵")

# --- MEMORIA ---
if 'galeria' not in st.session_state:
    st.session_state.galeria = []

# --- TÍTULO ---
st.title("🧵 Calculadora de Metraje")
st.markdown("Herramienta profesional para camisas de caballero.")

# --- PESTAÑAS ---
tab1, tab2 = st.tabs(["🧮 CALCULADORA", "📂 GALERÍA"])

# === PESTAÑA 1: CALCULADORA ===
with tab1:
    st.subheader("Ingresa las medidas")
    
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre del Cliente", placeholder="Ej. Juan Pérez")
        pecho = st.number_input("Pecho (cm)", min_value=50, max_value=200, value=99)
    with col2:
        largo_c = st.number_input("Largo Camisa (cm)", value=75)
        largo_m = st.number_input("Largo Manga (cm)", value=65)
    
    ancho_tela = st.select_slider("Ancho de la Tela (cm)", options=[90, 110, 140, 150, 160], value=150)

    if st.button("CALCULAR METRAJE ✂️"):
        # --- LÓGICA CORREGIDA ---
        
        # 1. CÁLCULO DEL LARGO (Tu fórmula)
        # Largo Camisa + Largo Manga + 5 (costura) + 10 (desperdicio) + 10 (piezas extra)
        total_cm = largo_c + largo_m + 5 + 10 + 10
        total_metros = total_cm / 100
        
        # 2. CÁLCULO DEL ANCHO (Lógica mejorada)
        # Asumimos que si el pecho + 30cm de holgura es menor al ancho de la tela, CABE.
        # Solo si es muy grande, pedimos doble.
        ancho_necesario_real = pecho + 30 
        
        if ancho_necesario_real > ancho_tela:
            cabe_en_tela = False
            mensaje_ancho = f"⚠️ El contorno es muy ancho ({pecho}cm). Mejor comprar DOBLE largo."
            total_metros = total_metros * 2 # Sugerimos comprar doble
        else:
            cabe_en_tela = True
            mensaje_ancho = "✅ El patrón cabe bien a lo ancho."

        # MOSTRAR RESULTADOS
        st.divider()
        st.markdown(f"### 🛍️ Resultado para: **{nombre}**")
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.metric(label="Metraje Sugerido", value=f"{total_metros:.2f} m")
        with col_res2:
            st.info(mensaje_ancho)

        # GUARDAR
        nuevo = {
            "Fecha": datetime.now().strftime("%d/%m/%Y"),
            "Cliente": nombre if nombre else "Anónimo",
            "Medidas": f"{pecho}/{largo_c}/{largo_m}",
            "Metraje": f"{total_metros:.2f} m",
            "Estado": "Doble" if not cabe_en_tela else "Estándar"
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
