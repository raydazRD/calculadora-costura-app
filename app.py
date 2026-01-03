import streamlit as st
import pandas as pd
from datetime import datetime
import math

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Calculadora Costura Pro", page_icon="🧵", layout="wide")

if 'galeria' not in st.session_state:
    st.session_state.galeria = []

# --- MENÚ LATERAL ---
st.sidebar.title("Menú Principal")
categoria = st.sidebar.radio("¿Qué deseas confeccionar?", 
                             ["👔 Camisería", "👗 Faldas", "📂 Galería"])
st.sidebar.divider()
st.sidebar.info("v2.0 - Módulos Avanzados")

# ==========================================
# 👔 MÓDULO CAMISERÍA (Caballero y Dama)
# ==========================================
if categoria == "👔 Camisería":
    st.title("👔 Taller de Camisería")
    
    # SUB-MENÚ: TIPO DE CAMISA
    tipo_camisa = st.selectbox("Estilo de Camisa:", 
                               ["Camisa Caballero Clásica", "Blusa Dama (Entallada/Mangas)"])
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Medidas")
        nombre = st.text_input("Nombre Cliente", key="nom_cam")
        pecho = st.number_input("Contorno Pecho/Busto (cm)", 50, 200, 100)
        largo_c = st.number_input("Largo Prenda (cm)", value=70)
        largo_m = st.number_input("Largo Manga (cm)", value=60)
        
    with col2:
        st.subheader("Tela y Detalles")
        ancho_tela = st.select_slider("Ancho Tela (cm)", [90, 110, 140, 150, 160], value=150)
        
        extra_manga = 0
        if tipo_camisa == "Blusa Dama (Entallada/Mangas)":
            estilo_manga = st.radio("Tipo de Manga:", ["Recta/Básica", "Campana/Volante"])
            if estilo_manga == "Campana/Volante":
                st.info("ℹ️ Se agregará 30cm extra por el vuelo de la manga.")
                extra_manga = 30 # Extra por manga campana
                
    if st.button("CALCULAR CAMISA ✂️"):
        # Fórmulas
        desperdicio = 25 # Costuras + márgenes estándar
        total_cm = largo_c + largo_m + desperdicio + extra_manga
        total_metros = total_cm / 100
        
        # Validación de Ancho
        # Dama suele ser más ajustada, Caballero más holgado
        holgura = 8 if "Dama" in tipo_camisa else 11
        ancho_nec = ((pecho / 4) + holgura) * 4 + 4
        
        st.divider()
        if ancho_nec > ancho_tela:
            st.warning(f"⚠️ El ancho del patrón ({ancho_nec}cm) supera la tela.")
            st.info("💡 Solución: Se calculó DOBLE tela.")
            total_metros = total_metros * 2
        else:
            st.success("✅ El patrón cabe bien en el ancho.")
            
        st.metric("Metraje a Comprar", f"{total_metros:.2f} m")
        
        # Guardar
        nuevo = {
            "Fecha": datetime.now().strftime("%d/%m"),
            "Prenda": tipo_camisa,
            "Cliente": nombre,
            "Detalles": f"Pecho:{pecho} L:{largo_c}",
            "Metraje": f"{total_metros:.2f} m"
        }
        st.session_state.galeria.append(nuevo)
        st.toast("Guardado", icon="💾")

# ==========================================
# 👗 MÓDULO FALDAS (Básica, Circular, Doble)
# ==========================================
elif categoria == "👗 Faldas":
    st.title("👗 Taller de Faldas")
    
    # SUB-MENÚ: TIPO DE FALDA
    tipo_falda = st.selectbox("Estilo de Falda:", 
                              ["Falda Básica (Recta/Tubo)", "Falda Circular (Plato)", "Falda Doble Circular"])
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Medidas")
        nombre = st.text_input("Nombre Cliente", key="nom_falda")
        cintura = st.number_input("Cintura (cm)", 40, 150, 70)
        # Solo pedimos cadera si es recta
        cadera = 0
        if tipo_falda == "Falda Básica (Recta/Tubo)":
            cadera = st.number_input("Cadera (cm)", 50, 200, 95)
            
        largo_f = st.number_input("Largo Falda (cm)", value=60)
        
    with col2:
        st.subheader("Tela")
        ancho_tela = st.select_slider("Ancho Tela (cm)", [90, 110, 140, 150, 160], value=150)
        st.caption("Para faldas circulares se recomienda tela de 150cm.")

    if st.button("CALCULAR FALDA ✂️"):
        st.divider()
        
        # --- LÓGICA SEGÚN TIPO ---
        
        if tipo_falda == "Falda Básica (Recta/Tubo)":
            # Fórmula Recta (La que ya validamos)
            largo_req = largo_f + 25 # Pretina, ruedo, margen
            metros = largo_req / 100
            ancho_nec = cadera + 10
            
            if ancho_nec > ancho_tela:
                st.warning("⚠️ Cadera ancha. Se requiere DOBLE largo.")
                metros = metros * 2
            else:
                st.success("✅ Cabe en el ancho.")
                
        elif tipo_falda == "Falda Circular (Plato)":
            # Fórmula Circular: Radio = Cintura / 6.28
            radio = cintura / 6.28
            largo_total_patron = largo_f + radio + 5 # +5 costuras
            diametro_total = largo_total_patron * 2
            
            st.info(f"ℹ️ Radio calculado: {radio:.1f} cm")
            
            if diametro_total <= ancho_tela:
                # Si el círculo entero cabe en el ancho de la tela
                metros = diametro_total / 100
                st.success("✅ La falda sale en una sola pieza (sin costuras laterales).")
            else:
                # Si no cabe, se corta en 2 semicírculos o se necesita doble largo
                st.warning(f"⚠️ El diámetro ({diametro_total:.0f}cm) es mayor que la tela.")
                metros = (largo_total_patron * 2) / 100
                st.info("💡 Cálculo para cortar en dos partes (semicírculos).")

        elif tipo_falda == "Falda Doble Circular":
            # Fórmula Doble Circular: 2 círculos completos
            # Radio más pequeño porque se divide la cintura en 2 círculos
            radio = (cintura / 2) / 6.28
            largo_total_patron = largo_f + radio + 5
            
            # Se necesitan al menos 2 cuadrados de tela grandes
            metros = (largo_total_patron * 2 * 2) / 100
            st.info(f"ℹ️ Falda de mucho vuelo (2 rotondas). Radio: {radio:.1f} cm")
            st.success("✅ Cálculo para 2 círculos completos.")

        # RESULTADO FINAL
        st.metric("Metraje a Comprar", f"{metros:.2f} m")
        
        # Guardar
        nuevo = {
            "Fecha": datetime.now().strftime("%d/%m"),
            "Prenda": tipo_falda,
            "Cliente": nombre,
            "Detalles": f"Cint:{cintura} L:{largo_f}",
            "Metraje": f"{metros:.2f} m"
        }
        st.session_state.galeria.append(nuevo)
        st.toast("Guardado", icon="💾")

# ==========================================
# 📂 GALERÍA
# ==========================================
elif categoria == "📂 Galería":
    st.header("📂 Historial")
    if st.session_state.galeria:
        st.dataframe(pd.DataFrame(st.session_state.galeria), use_container_width=True)
        if st.button("Borrar Historial"):
            st.session_state.galeria = []
            st.rerun()
    else:
        st.info("Historial vacío.")
