import streamlit as st
from pydub import AudioSegment
import io

# Configuración básica de la página
st.set_page_config(page_title="Convertidor M4A a MP3", page_icon="🎵")

st.title("🎵 Convertidor de M4A a MP3")
st.write("Sube tus archivos de audio en formato `.m4a` y descárgalos en `.mp3` fácilmente.")

# Selector de archivos (permite múltiples)
archivos_subidos = st.file_uploader(
    "Arrastra tus archivos aquí o haz clic para buscar", 
    type=["m4a"], 
    accept_multiple_files=True
)

# Si el usuario ha subido archivos
if archivos_subidos:
    st.markdown("---")
    st.write("### Progreso de conversión")
    
    # Iterar sobre cada archivo subido
    for i, archivo in enumerate(archivos_subidos):
        # Generar el nuevo nombre del archivo
        nombre_mp3 = archivo.name.replace(".m4a", ".mp3")
        # Ignorar mayúsculas en la extensión por si acaso (.M4A)
        nombre_mp3 = nombre_mp3.replace(".M4A", ".mp3") 
        
        # Crear columnas para organizar mejor la interfaz
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.write(f"🎧 **{archivo.name}**")
            
        with col2:
            try:
                # Usar un spinner visual mientras se convierte
                with st.spinner("Convirtiendo..."):
                    # 1. Leer el archivo directamente de la memoria de Streamlit
                    audio = AudioSegment.from_file(archivo, format="m4a")
                    
                    # 2. Crear un espacio en memoria para el archivo de salida
                    buffer_mp3 = io.BytesIO()
                    
                    # 3. Exportar el audio convertido a ese espacio en memoria
                    audio.export(buffer_mp3, format="mp3", bitrate="192k")
                    
                    # 4. Mostrar el botón de descarga
                    st.download_button(
                        label=f"⬇️ Descargar MP3",
                        data=buffer_mp3,
                        file_name=nombre_mp3,
                        mime="audio/mpeg",
                        key=f"descarga_{i}" # Clave única obligatoria en Streamlit
                    )
            except Exception as e:
                st.error(f"Error: {e}. ¿Tienes FFmpeg instalado?")

    st.success("¡Todos los archivos han sido procesados!")