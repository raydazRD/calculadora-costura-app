import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Calculadora Costura Pro", page_icon="🧵", layout="wide")

# --- MEMORIA (Base de datos temporal) ---
if 'galeria' not in st.session_state:
    st.session_state.galeria = []

# --- BARRA LATERAL (EL MENÚ) ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4327/4327365.png", width=100)
st.sidebar.title("Menú Principal")
modo = st.sidebar.radio("Selecciona una opción:", ["👔 Camisa Caballero", "👗 Falda Básica", "📂 Galería/Historial"])

st.sidebar.divider()
st.sidebar.info("Versión Beta 1.3")

# ==========================================
# 👔 MÓDULO 1: CAMISA DE CABALLERO
# ==========================================
if modo == "👔 Camisa Caballero":
    st.title("👔 Calculadora: Camisa Caballero")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Medidas")
        nombre = st.text_input("Nombre Cliente", key="nom_camisa")
        pecho = st.number_input("Pecho (cm)", 50, 200, 100)
        largo_c = st.number_input("Largo Camisa (cm)", value=75)
        largo_m = st.number_input("Largo Manga (cm)", value=65)
    
    with col2:
        st.subheader("Tela")
        ancho_tela = st.select_slider("Ancho Tela (cm)", [90, 110, 140, 150, 160], value=150, key="ancho_camisa")
        imagen = st.file_uploader("Foto Referencia", type=['jpg','png'], key="img_camisa")
        if imagen: st.image(imagen, width=200)

    if st.button("CALCULAR CAMISA ✂️"):
        # Fórmulas Camisa
        total_cm = largo_c + largo_m + 25
        total_metros = total_cm / 100
        
        # Fórmula Ancho (Tu ajuste de 4cm)
        ancho_necesario = ((pecho / 4) + 11) * 4 + 4 
        
        if ancho_necesario > ancho_tela:
            msg = f"⚠️ Ancho insuficiente ({ancho_necesario}cm). Se calculó DOBLE tela."
            total_metros = total_metros * 2
            estado = "Doble"
            st.error(msg)
        else:
            msg = "✅ El patrón cabe bien."
            estado = "Estándar"
            st.success(msg)
            
        st.metric("Metraje a Comprar", f"{total_metros:.2f} m")
        
        # Guardar
        nuevo = {
            "Fecha": datetime.now().strftime("%d/%m"),
            "Prenda": "Camisa",
            "Cliente": nombre,
            "Detalles": f"Pecho: {pecho}",
            "Metraje": f"{total_metros:.2f} m"
        }
        st.session_state.galeria.append(nuevo)
        st.toast("Guardado", icon="💾")

# ==========================================
# 👗 MÓDULO 2: FALDA BÁSICA (CORREGIDO)
# ==========================================
elif modo == "👗 Falda Básica":
    st.title("👗 Calculadora: Falda Básica")
    st.info("Cálculo para falda recta clásica.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Medidas")
        nombre = st.text_input("Nombre Cliente", key="nom_falda")
        cintura = st.number_input("Cintura (cm)", 40, 150, 70)
        cadera = st.number_input("Cadera (cm)", 50, 200, 95)
        largo_f = st.number_input("Largo Falda (cm)", value=60)
    
    with col2:
        st.subheader("Tela")
        ancho_tela = st.select_slider("Ancho Tela (cm)", [90, 110, 140, 150, 160], value=150, key="ancho_falda")
        imagen_f = st.file_uploader("Foto Referencia", type=['jpg','png'], key="img_falda")
        if imagen_f: st.image(imagen_f, width=200)

    if st.button("CALCULAR FALDA ✂️"):
        # --- FÓRMULA FALDA ACTUALIZADA ---
        # 1. Largo: Largo + 10 (pretina) + 5 (ruedo) + 10 (desperdicio)
        largo_total_cm = largo_f + 10 + 5 + 10
        metros = largo_total_cm / 100
        
        # 2. Ancho: Cadera + 5 (holgura) + 5 (costura)
        ancho_total_patron = cadera + 5 + 5
        
        st.divider()
        st.markdown(f"### Resultado para {nombre if nombre else 'Cliente'}")

        # Lógica de decisión
        if ancho_total_patron > ancho_tela:
            st.warning(f"⚠️ El ancho requerido ({ancho_total_patron} cm) es mayor que la tela ({ancho_tela} cm).")
            st.info("💡 Solución: Se requiere DOBLE largo de tela.")
            metros = metros * 2
        else:
            st.success(f"✅ El ancho ({ancho_total_patron} cm) cabe perfectamente en la tela.")
            
        st.metric("Metraje a Comprar", f"{metros:.2f} m")
        
        # Guardar
        nuevo = {
            "Fecha": datetime.now().strftime("%d/%m"),
            "Prenda": "Falda",
            "Cliente": nombre,
            "Detalles": f"Cadera: {cadera} / Largo: {largo_f}",
            "Metraje": f"{metros:.2f} m"
        }
        st.session_state.galeria.append(nuevo)
        st.toast("Guardado", icon="💾")

# ==========================================
# 📂 MÓDULO 3: GALERÍA
# ==========================================
elif modo == "📂 Galería/Historial":
    st.header("📂 Historial de Proyectos")
    
    if len(st.session_state.galeria) > 0:
        df = pd.DataFrame(st.session_state.galeria)
        st.dataframe(df, use_container_width=True)
        
        if st.button("Borrar todo el historial"):
            st.session_state.galeria = []
            st.rerun()
    else:
        st.info("No hay mediciones guardadas en esta sesión.")
