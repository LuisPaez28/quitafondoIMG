import streamlit as st
from rembg import remove
from PIL import Image
import io

# 1. Configuración de la página
st.set_page_config(page_title="QuitaFondo", page_icon="✨")

st.title("Removedor de Fondos")
st.write("Sube tu imagen para remover el fondo")

# 2. El Widget de carga de archivos (Reemplaza al botón 'Seleccionar')
uploaded_file = st.file_uploader("Elige una imagen (JPG, PNG, WEBP)", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    # Mostrar la imagen original
    image = Image.open(uploaded_file)
    
    # Crear dos columnas para ver el Antes y Después
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Original")
        st.image(image, use_container_width=True)

    # 3. Procesamiento (La Magia)
    with col2:
        st.header("Sin Fondo")
        
        # Botón para activar la IA
        if st.button("Quitar Fondo"):
            with st.spinner("La IA está trabajando..."):
                # Convertir imagen a bytes
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                byte_im = buf.getvalue()
                
                # Procesar con rembg
                output_bytes = remove(byte_im)
                
                # Convertir resultado a imagen para mostrar
                output_image = Image.open(io.BytesIO(output_bytes))
                
                st.image(output_image, use_container_width=True)
                
                # 4. Botón de Descarga
                st.download_button(
                    label="Descargar Imagen PNG",
                    data=output_bytes,
                    file_name="sin_fondo.png",
                    mime="image/png"
                )