import streamlit as st
import subprocess
import tempfile
import os

# Configuración básica de la página
st.set_page_config(page_title="Convertidor a MP3", page_icon="🎵")

st.title("🎵 Convertidor Universal a MP3")
# Actualizamos la descripción para incluir .ogg
st.write("Sube tus archivos de audio (`.m4a`, `.ogg`) o video (`.mp4`) y extrae el audio en `.mp3` fácilmente.")

# Selector de calidad
calidad_opcion = st.selectbox(
    "Selecciona la calidad del audio:",
    ("Alta (320 kbps) - Mejor sonido, archivo más pesado", 
     "Media (192 kbps) - Buen equilibrio", 
     "Baja (128 kbps) - Archivo ligero")
)

bitrates = {
    "Alta (320 kbps) - Mejor sonido, archivo más pesado": "320k",
    "Media (192 kbps) - Buen equilibrio": "192k",
    "Baja (128 kbps) - Archivo ligero": "128k"
}
bitrate_elegido = bitrates[calidad_opcion]

# --- NUEVO: Agregamos "ogg" a los tipos permitidos ---
archivos_subidos = st.file_uploader(
    "Arrastra tus archivos aquí o haz clic para buscar", 
    type=["m4a", "mp4", "ogg"], 
    accept_multiple_files=True
)
# ------------------------------------------------------

if archivos_subidos:
    st.markdown("---")
    st.write("### Progreso de conversión")
    
    for i, archivo in enumerate(archivos_subidos):
        ext_original = os.path.splitext(archivo.name)[1].lower()
        nombre_mp3 = archivo.name.lower().replace(ext_original, ".mp3")
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            icono = "🎬" if ext_original == ".mp4" else "🎧"
            st.write(f"{icono} **{archivo.name}**")
            
        with col2:
            with st.spinner("Procesando..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=ext_original) as temp_in:
                        temp_in.write(archivo.read())
                        temp_in_path = temp_in.name
                        
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_out:
                        temp_out_path = temp_out.name

                    # Ejecutar FFmpeg
                    comando = [
                        "ffmpeg", 
                        "-y",             
                        "-i", temp_in_path, 
                        "-b:a", bitrate_elegido,
                        temp_out_path     
                    ]
                    
                    subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

                    with open(temp_out_path, "rb") as f:
                        mp3_data = f.read()

                    st.download_button(
                        label=f"⬇️ Descargar MP3",
                        data=mp3_data,
                        file_name=nombre_mp3,
                        mime="audio/mpeg",
                        key=f"descarga_{i}"
                    )
                    
                except subprocess.CalledProcessError:
                    st.error("Error en la conversión con FFmpeg.")
                except Exception as e:
                    st.error(f"Ocurrió un error: {e}")
                finally:
                    if os.path.exists(temp_in_path): os.remove(temp_in_path)
                    if os.path.exists(temp_out_path): os.remove(temp_out_path)

    st.success("¡Todos los archivos han sido procesados con éxito!")