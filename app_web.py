import streamlit as st
from rembg import remove, new_session
from PIL import Image
import io

# 1. Configuración de la página
st.set_page_config(page_title="QuitaFondo", page_icon="✨")

st.title("Removedor de Fondos")
st.write("Sube tu imagen para remover el fondo")

# Inicializar el estado de sesión
if "output_bytes" not in st.session_state:
    st.session_state.output_bytes = None

# 2. El Widget de carga de archivos
uploaded_file = st.file_uploader("Elige una imagen (JPG, PNG, WEBP)", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Original")
        # Regresamos a width='stretch' como pedía tu terminal
        st.image(image, width="stretch")

    # 3. Procesamiento
    with col2:
        st.header("Sin Fondo")
        
        if st.button("Quitar Fondo"):
            with st.spinner("Descargando modelo ligero y procesando..."):
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                byte_im = buf.getvalue()
                
                # CREAMOS UNA SESIÓN CON EL MODELO LIGERO 'u2netp' PARA NO SATURAR LA RAM
                my_session = new_session("u2netp")
                
                # Le pasamos la sesión a la función remove
                st.session_state.output_bytes = remove(byte_im, session=my_session)
        
        # 4. Mostrar y Descargar
        if st.session_state.output_bytes is not None:
            output_image = Image.open(io.BytesIO(st.session_state.output_bytes))
            st.image(output_image, width="stretch")
            
            st.download_button(
                label="Descargar Imagen PNG",
                data=st.session_state.output_bytes,
                file_name="sin_fondo.png",
                mime="image/png"
            )
else:
    st.session_state.output_bytes = None