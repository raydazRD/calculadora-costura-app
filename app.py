import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Calculadora Costura Pro", page_icon="🧵", layout="wide")

if 'galeria' not in st.session_state:
    st.session_state.galeria = []

# --- SIDEBAR (Menú Lateral) ---
st.sidebar.title("Menú Principal")

# 1. GÉNERO
genero = st.sidebar.selectbox("1. Selecciona el Género", 
                              ["👨 Caballero (Burda)", "👩 Dama", "👶 Niños", "📂 Historial"])

# 2. CATEGORÍA (Estructura Burda Style)
categoria_prenda = "Inicio"
tipo_especifico = "Estándar"

if genero == "👨 Caballero (Burda)":
    st.sidebar.markdown("---")
    st.sidebar.subheader("2. Categoría")
    categoria_prenda = st.sidebar.radio("Selecciona categoría:", 
        ["Camisas", 
         "Pantalones & Shorts", 
         "Chaquetas & Abrigos", 
         "Americanas & Trajes", 
         "Sudaderas & Sport",
         "Chalecos"])

st.sidebar.divider()
st.sidebar.info("v4.0 - Estructura Burda Style")

# ==========================================
# 👨 MÓDULO CABALLERO (LOGICA COMPLETA)
# ==========================================
if genero == "👨 Caballero (Burda)":
    st.title(f"👨 Caballero: {categoria_prenda}")
    
    # --- VARIABLES DE ENTRADA (DINÁMICAS) ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Medidas del Cliente")
        nombre = st.text_input("Nombre Cliente", key="nom_cab")
        
        # DEFINIR QUÉ MEDIDAS PEDIR SEGÚN LA CATEGORÍA
        # Variables por defecto
        pecho = 0
        cadera = 0
        largo_prenda = 0
        largo_manga = 0
        
        if categoria_prenda in ["Camisas", "Chaquetas & Abrigos", "Americanas & Trajes", "Sudaderas & Sport", "Chalecos"]:
            pecho = st.number_input("Contorno Pecho (cm)", 80, 170, 100)
            
        if categoria_prenda in ["Pantalones & Shorts", "Sudaderas & Sport", "Americanas & Trajes"]:
            cadera = st.number_input("Contorno Cadera (cm)", 80, 170, 100)

        # Largos sugeridos según prenda
        val_largo = 75 # Default camisa
        val_manga = 62 # Default manga
        
        if categoria_prenda == "Pantalones & Shorts":
            tipo_especifico = st.radio("Tipo:", ["Pantalón Largo", "Short/Bermuda"])
            val_largo = 105 if tipo_especifico == "Pantalón Largo" else 55
            val_manga = 0 # No usa manga
            
        elif categoria_prenda == "Chaquetas & Abrigos":
            tipo_especifico = st.radio("Tipo:", ["Chaqueta/Cazadora", "Abrigo Largo"])
            val_largo = 70 if tipo_especifico == "Chaqueta/Cazadora" else 100
            
        elif categoria_prenda == "Americanas & Trajes":
            tipo_especifico = st.radio("Tipo:", ["Solo Americana (Saco)", "Traje Completo (Saco + Pantalón)"])
            val_largo = 75 # Largo del Saco
            
        elif categoria_prenda == "Chalecos":
            val_largo = 60
            val_manga = 0
            
        # Inputs de Largo
        largo_prenda = st.number_input(f"Largo Prenda (cm)", value=val_largo)
        
        if categoria_prenda not in ["Pantalones & Shorts", "Chalecos"]:
            largo_manga = st.number_input("Largo Manga (cm)", value=val_manga)

    with col2:
        st.subheader("Configuración Tela")
        ancho_tela = st.select_slider("Ancho Tela (cm)", [110, 140, 150, 160], value=150)
        
        # CHECKBOX DE EXTRAS
        st.markdown("**Detalles Extra:**")
        check_cuadros = st.checkbox("Tela con cuadros/rayas (+10%)")
        check_capucha = False
        if categoria_prenda == "Sudaderas & Sport":
            check_capucha = st.checkbox("Lleva Capucha (+40cm)")

    # --- BOTÓN Y CÁLCULOS ---
    if st.button("CALCULAR CONSUMO ✂️"):
        metros = 0
        notas = []
        
        # 1. CAMISAS
        if categoria_prenda == "Camisas":
            total_cm = largo_prenda + largo_manga + 25 # Cuello, puños
            metros = total_cm / 100
            # Validación Ancho
            if ((pecho/4)+10)*4 + 4 > ancho_tela:
                metros *= 2
                notas.append("⚠️ Se calculó doble por ancho de pecho.")

        # 2. PANTALONES & SHORTS
        elif categoria_prenda == "Pantalones & Shorts":
            total_cm = largo_prenda + 20 # Pretina, bolsillos, ruedo
            metros = total_cm / 100
            # Validación Cadera
            if (cadera/2) + 10 > (ancho_tela - 5):
                metros *= 2
                notas.append("⚠️ Cadera ancha. Se requiere doble largo.")

        # 3. CHAQUETAS & ABRIGOS
        elif categoria_prenda == "Chaquetas & Abrigos":
            # Consumo mayor por vistas, cuellos y solapas
            extra_vistas = 30 if tipo_especifico == "Abrigo Largo" else 20
            total_cm = largo_prenda + largo_manga + extra_vistas
            metros = total_cm / 100
            notas.append("ℹ️ Incluye margen para vistas y solapas.")

        # 4. AMERICANAS & TRAJES
        elif categoria_prenda == "Americanas & Trajes":
            # Consumo Americana
            cons_saco = largo_prenda + largo_manga + 20
            
            if tipo_especifico == "Solo Americana (Saco)":
                metros = cons_saco / 100
            else: # Traje Completo
                # Saco + Pantalón
                cons_pantalon = 110 + 20 # Estimado pantalón estándar
                metros = (cons_saco + cons_pantalon) / 100
                notas.append("ℹ️ Cálculo: Saco + Pantalón.")

        # 5. SUDADERAS
        elif categoria_prenda == "Sudaderas & Sport":
            total_cm = largo_prenda + largo_manga + 15
            if check_capucha:
                total_cm += 40
                notas.append("ℹ️ Incluye +40cm para capucha.")
            metros = total_cm / 100

        # 6. CHALECOS
        elif categoria_prenda == "Chalecos":
            total_cm = largo_prenda + 15 # Vistas internas
            metros = total_cm / 100
            notas.append("ℹ️ Sin mangas.")

        # --- AJUSTE POR CUADROS/RAYAS ---
        if check_cuadros:
            metros = metros * 1.10
            notas.append("⚠️ +10% agregado por casar cuadros/rayas.")

        # MOSTRAR RESULTADOS
        st.divider()
        st.metric("Metraje a Comprar", f"{metros:.2f} m")
        
        for n in notas:
            st.info(n)

        # GUARDAR
        nuevo = {
            "Fecha": datetime.now().strftime("%d/%m"),
            "Cliente": nombre,
            "Prenda": f"{categoria_prenda} ({tipo_especifico})",
            "Metraje": f"{metros:.2f} m"
        }
        st.session_state.galeria.append(nuevo)
        st.toast("Guardado")

# ==========================================
# 👩 DAMA / NIÑOS / HISTORIAL (Placeholders)
# ==========================================
elif genero == "👩 Dama":
    st.title("👩 Dama")
    st.info("Módulo Dama pendiente de estructurar igual que Caballero.")

elif genero == "📂 Historial":
    st.header("📂 Historial")
    if st.session_state.galeria:
        st.dataframe(pd.DataFrame(st.session_state.galeria), use_container_width=True)
        if st.button("Borrar Todo"):
            st.session_state.galeria = []
            st.rerun()
