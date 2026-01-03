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
    col_izq, col_der = st.columns(2)
    
    with col_izq:
        st.subheader("1. Medidas del Cliente")
        nombre = st.text_input("Nombre del Cliente", placeholder="Ej. Juan Pérez")
        pecho = st.number_input("Pecho (cm)", min_value=50, max_value=200, value=99)
        largo_c = st.number_input("Largo Camisa (cm)", value=75)
        largo_m = st.number_input("Largo Manga (cm)", value=65)
        
    with col_der:
        st.subheader("2. Detalles de la Tela")
        ancho_tela = st.select_slider("Ancho de la Tela (cm)", options=[90, 110, 140, 150, 160], value=150)
        
        # --- NUEVO: CARGAR IMAGEN ---
        st.markdown("---")
        st.markdown("📸 **Referencia Visual**")
        imagen = st.file_uploader("Sube foto de la tela o modelo", type=['png', 'jpg', 'jpeg'])
        if imagen is not None:
            st.image(imagen, caption="Modelo de referencia", use_column_width=True)

    # --- BOTÓN DE CÁLCULO ---
    st.markdown("---")
    if st.button("CALCULAR METRAJE ✂️", type="primary"):
        # 1. CÁLCULO LARGO
        total_cm = largo_c + largo_m + 5 + 10 + 10
        total_metros = total_cm / 100
        
        # 2. CÁLCULO ANCHO (Tu fórmula ajustada)
        ancho_pieza = (pecho / 4) + 6 + 5
        ancho_total_cuerpo = (ancho_pieza * 4) + 4  # 4cm de separación
        
        if ancho_total_cuerpo > ancho_tela:
            cabe_en_tela = False
            mensaje_ancho = f"⚠️ El patrón ocupa {ancho_total_cuerpo}cm. ¡Es muy ancho!"
            total_metros = total_metros * 2
            nota_final = "⚠️ Doble Tela"
        else:
            cabe_en_tela = True
            mensaje_ancho = f"✅ El patrón ocupa {ancho_total_cuerpo}cm. Cabe bien."
            nota_final = "✅ Estándar"

        # RESULTADOS
        st.success(f"### 🛍️ Comprar: {total_metros:.2f} metros")
        if not cabe_en_tela:
            st.warning(f"{mensaje_ancho} (Se calculó doble largo).")
        else:
            st.info(mensaje_ancho)

        # GUARDAR EN HISTORIAL
        nuevo_id = len(st.session_state.galeria) + 1
        nuevo = {
            "ID": nuevo_id,
            "Fecha": datetime.now().strftime("%d/%m/%Y"),
            "Cliente": nombre if nombre else "Anónimo",
            "Medidas": f"P:{pecho} / LC:{largo_c} / LM:{largo_m}",
            "Metraje": f"{total_metros:.2f} m",
            "Nota": nota_final
        }
        st.session_state.galeria.append(nuevo)
        st.toast("Guardado en Galería", icon="💾")

# === PESTAÑA 2: GALERÍA (Edición) ===
with tab2:
    st.header("📂 Historial de Proyectos")
    
    if len(st.session_state.galeria) > 0:
        # Convertimos a tabla
        df = pd.DataFrame(st.session_state.galeria)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.divider()
        st.subheader("🗑️ Gestión de registros")
        
        # Selector para borrar
        lista_clientes = [f"{item['ID']} - {item['Cliente']}" for item in st.session_state.galeria]
        seleccion = st.selectbox("Seleccionar registro a eliminar:", options=lista_clientes)
        
        if st.button("Eliminar Registro Seleccionado"):
            # Lógica para borrar
            id_a_borrar = int(seleccion.split(" - ")[0])
            st.session_state.galeria = [d for d in st.session_state.galeria if d['ID'] != id_a_borrar]
            st.rerun() # Recarga la página para ver cambios
            
    else:
        st.info("Aún no hay proyectos guardados en esta sesión.")
