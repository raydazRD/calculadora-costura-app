import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN GENERAL ---
st.set_page_config(page_title="Calculadora Costura Pro", page_icon="🧵", layout="wide")

if 'galeria' not in st.session_state:
    st.session_state.galeria = []

# ==========================================
# 🟩 MENÚ LATERAL (SIDEBAR)
# ==========================================
st.sidebar.title("🪡 Menú Taller")

# 1. SELECCIÓN DE GÉNERO
genero = st.sidebar.selectbox("1. Departamento", 
                              ["👨 Caballero", "👩 Dama", "👶 Infantil/Bebés", "📂 Historial"])

st.sidebar.markdown("---")

# 2. SELECCIÓN DE PRENDA (DINÁMICA)
categoria_prenda = "Inicio"
sub_tipo = "Estándar"

# --- MENÚ CABALLERO ---
if genero == "👨 Caballero":
    st.sidebar.header("Prendas Caballero")
    categoria_prenda = st.sidebar.radio("Selecciona:", 
        ["Camisas", "Pantalones & Shorts", "Chaquetas & Abrigos", 
         "Trajes (Saco/Pantalón)", "Sudaderas & Sport", "Chalecos"])

# --- MENÚ DAMA ---
elif genero == "👩 Dama":
    st.sidebar.header("Prendas Dama")
    categoria_prenda = st.sidebar.radio("Selecciona:", 
        ["Blusas & Tops", "Faldas", "Vestidos & Enterizos", 
         "Pantalones & Shorts", "Chaquetas & Blazers"])

# --- MENÚ INFANTIL ---
elif genero == "👶 Infantil/Bebés":
    st.sidebar.header("Prendas Infantil")
    categoria_prenda = st.sidebar.radio("Selecciona:", 
        ["Bebés (0-24 meses)", "Niña (2-14 años)", "Niño (2-14 años)"])

st.sidebar.divider()
st.sidebar.info("v5.0 - Multi-Género")


# ==========================================
# 🟧 LÓGICA PRINCIPAL DE CÁLCULO
# ==========================================
if genero != "📂 Historial":
    st.title(f"{genero}: {categoria_prenda}")
    
    col1, col2 = st.columns(2)
    
    # --- COLUMNA 1: MEDIDAS ---
    with col1:
        st.subheader("📏 Medidas")
        nombre = st.text_input("Nombre Cliente")
        
        # Variables iniciales
        largo_prenda = 0
        largo_manga = 0
        contorno_ref = 0 # Puede ser pecho, busto o cadera
        
        # --- INPUTS CABALLERO ---
        if genero == "👨 Caballero":
            if categoria_prenda in ["Pantalones & Shorts"]:
                contorno_ref = st.number_input("Contorno Cadera (cm)", 50, 180, 100)
                sub_tipo = st.radio("Largo:", ["Pantalón Largo", "Short/Bermuda"])
                largo_prenda = st.number_input("Largo Lateral (cm)", value=105 if "Largo" in sub_tipo else 55)
            else:
                contorno_ref = st.number_input("Contorno Pecho (cm)", 50, 180, 100)
                largo_prenda = st.number_input("Largo Prenda (cm)", value=75)
                if categoria_prenda not in ["Chalecos"]:
                    largo_manga = st.number_input("Largo Manga (cm)", value=62)

        # --- INPUTS DAMA ---
        elif genero == "👩 Dama":
            if categoria_prenda == "Faldas":
                contorno_ref = st.number_input("Contorno Cintura (cm)", 40, 140, 70)
                cadera_aux = st.number_input("Contorno Cadera (cm)", 50, 180, 95)
                sub_tipo = st.selectbox("Estilo:", ["Recta/Básica", "Circular (Plato)", "Doble Circular"])
                largo_prenda = st.number_input("Largo Falda (cm)", value=60)
                
            elif categoria_prenda == "Vestidos & Enterizos":
                contorno_ref = st.number_input("Contorno Busto (cm)", 50, 180, 90)
                cadera_aux = st.number_input("Contorno Cadera (cm)", 50, 180, 95) # Para validar ancho
                sub_tipo = st.radio("Estilo:", ["Corto", "Largo", "Fiesta (Con vuelo)"])
                largo_prenda = st.number_input("Largo Total (cm)", value=100)
                largo_manga = st.number_input("Largo Manga (cm)", value=20)
                
            elif categoria_prenda == "Pantalones & Shorts":
                contorno_ref = st.number_input("Contorno Cadera (cm)", 50, 180, 95)
                largo_prenda = st.number_input("Largo Lateral (cm)", value=100)
                
            else: # Blusas, Chaquetas
                contorno_ref = st.number_input("Contorno Busto (cm)", 50, 180, 90)
                largo_prenda = st.number_input("Largo Prenda (cm)", value=60)
                largo_manga = st.number_input("Largo Manga (cm)", value=58)

        # --- INPUTS INFANTIL ---
        elif genero == "👶 Infantil/Bebés":
            sub_tipo = st.selectbox("Prenda:", ["Camisa/Blusa", "Pantalón", "Vestido", "Conjunto Completo"])
            largo_prenda = st.number_input("Largo Principal (cm)", value=40)
            if "Pantalón" not in sub_tipo:
                largo_manga = st.number_input("Largo Manga (cm)", value=30)

    # --- COLUMNA 2: TELA Y EXTRAS ---
    with col2:
        st.subheader("✂️ Tela")
        ancho_tela = st.select_slider("Ancho Tela (cm)", [110, 140, 150, 160], value=150)
        
        st.markdown("---")
        st.caption("Ajustes Especiales")
        check_cuadros = st.checkbox("Tela a Cuadros/Rayas (+10%)")
        check_holgura = st.checkbox("Diseño Oversize/Holgado")
        
    # --- BOTÓN DE CÁLCULO ---
    if st.button("CALCULAR CONSUMO ✂️", type="primary"):
        metros = 0
        notas = []
        
        # === CÁLCULOS CABALLERO ===
        if genero == "👨 Caballero":
            if categoria_prenda == "Trajes (Saco/Pantalón)":
                metros = (largo_prenda + largo_manga + 20 + 110 + 20) / 100 # Saco + Pantalon est.
                notas.append("Incluye Saco y Pantalón.")
            elif categoria_prenda == "Sudaderas & Sport":
                metros = (largo_prenda + largo_manga + 40 + 20) / 100 # +Capucha
            else:
                metros = (largo_prenda + largo_manga + 20) / 100

        # === CÁLCULOS DAMA ===
        elif genero == "👩 Dama":
            if categoria_prenda == "Faldas":
                if sub_tipo == "Circular (Plato)":
                    radio = contorno_ref / 6.28
                    diametro = (largo_prenda + radio) * 2
                    if diametro <= ancho_tela:
                        metros = diametro / 100
                        notas.append("Sale en una pieza (Círculo completo).")
                    else:
                        metros = (diametro / 100) 
                        notas.append("Se requiere cortar en 2 partes (Semicírculos).")
                elif sub_tipo == "Doble Circular":
                    radio = (contorno_ref/2) / 6.28
                    metros = ((largo_prenda + radio) * 4) / 100
                else: # Recta
                    metros = (largo_prenda + 15) / 100
                    if cadera_aux + 10 > ancho_tela: metros *= 2
            
            elif categoria_prenda == "Vestidos & Enterizos":
                metros = (largo_prenda + largo_manga + 25) / 100
                if sub_tipo == "Fiesta (Con vuelo)":
                    metros *= 1.5 # Estimación vuelo
                    notas.append("Ajuste por vuelo de falda.")
            else:
                metros = (largo_prenda + largo_manga + 20) / 100

        # === CÁLCULOS INFANTIL ===
        elif genero == "👶 Infantil/Bebés":
            margen_nino = 15
            if sub_tipo == "Conjunto Completo":
                metros = (largo_prenda * 2 + largo_manga + margen_nino) / 100
            else:
                metros = (largo_prenda + largo_manga + margen_nino) / 100

        # === AJUSTES GLOBALES ===
        # 1. Validación de Ancho (Genérica para prendas superiores)
        if categoria_prenda not in ["Faldas", "Pantalones & Shorts"] and genero != "👶 Infantil/Bebés":
            if ((contorno_ref / 4) + 10) * 4 + 4 > ancho_tela:
                if "Doble" not in "".join(notas): # Evitar doble penalización
                    metros *= 2
                    notas.append("⚠️ Se calculó doble por ancho del cuerpo.")

        # 2. Ajuste Cuadros
        if check_cuadros:
            metros *= 1.10
            notas.append("✅ +10% por casar cuadros.")
            
        # 3. Ajuste Oversize
        if check_holgura:
            metros += 0.20
            notas.append("✅ +20cm holgura diseño.")

        # MOSTRAR RESULTADO
        st.divider()
        st.success(f"### 🛍️ Comprar: {metros:.2f} metros")
        for n in notas: st.info(n)
        
        # GUARDAR
        nuevo = {
            "Fecha": datetime.now().strftime("%d/%m"),
            "Cliente": nombre if nombre else "Anónimo",
            "Prenda": f"{genero[0]} {categoria_prenda} ({sub_tipo})",
            "Metraje": f"{metros:.2f} m"
        }
        st.session_state.galeria.append(nuevo)
        st.toast("Guardado en Historial")

# ==========================================
# 📂 HISTORIAL
# ==========================================
else:
    st.header("📂 Historial de Proyectos")
    if st.session_state.galeria:
        df = pd.DataFrame(st.session_state.galeria)
        st.dataframe(df, use_container_width=True)
        if st.button("🗑️ Borrar Historial"):
            st.session_state.galeria = []
            st.rerun()
    else:
        st.info("No hay registros aún.")
