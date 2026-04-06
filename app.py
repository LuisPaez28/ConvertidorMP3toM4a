import streamlit as st
import subprocess
import tempfile
import os

# Configuración básica de la página
st.set_page_config(page_title="Convertidor M4A a MP3", page_icon="🎵")

st.title("🎵 Convertidor de M4A a MP3")
st.write("Sube tus archivos de audio en formato `.m4a` y descárgalos en `.mp3` fácilmente.")

# Selector de archivos
archivos_subidos = st.file_uploader(
    "Arrastra tus archivos aquí o haz clic para buscar", 
    type=["m4a"], 
    accept_multiple_files=True
)

if archivos_subidos:
    st.markdown("---")
    st.write("### Progreso de conversión")
    
    for i, archivo in enumerate(archivos_subidos):
        # Generar el nuevo nombre del archivo
        nombre_mp3 = archivo.name.lower().replace(".m4a", ".mp3")
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.write(f"🎧 **{archivo.name}**")
            
        with col2:
            with st.spinner("Convirtiendo..."):
                try:
                    # 1. Crear archivos temporales seguros para que FFmpeg los lea
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".m4a") as temp_in:
                        temp_in.write(archivo.read())
                        temp_in_path = temp_in.name
                        
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_out:
                        temp_out_path = temp_out.name

                    # 2. Ejecutar FFmpeg directamente desde el sistema
                    comando = [
                        "ffmpeg", 
                        "-y",             # Sobrescribir si existe
                        "-i", temp_in_path, # Archivo de entrada
                        "-b:a", "192k",   # Calidad del MP3
                        temp_out_path     # Archivo de salida
                    ]
                    
                    # Ejecutar la orden
                    subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

                    # 3. Leer el MP3 resultante para ofrecer la descarga
                    with open(temp_out_path, "rb") as f:
                        mp3_data = f.read()

                    # 4. Mostrar el botón de descarga
                    st.download_button(
                        label=f"⬇️ Descargar MP3",
                        data=mp3_data,
                        file_name=nombre_mp3,
                        mime="audio/mpeg",
                        key=f"descarga_{i}"
                    )
                    
                except subprocess.CalledProcessError as e:
                    st.error("Error en la conversión con FFmpeg.")
                except Exception as e:
                    st.error(f"Ocurrió un error: {e}")
                finally:
                    # 5. Limpiar los archivos temporales para no saturar el servidor
                    if os.path.exists(temp_in_path): os.remove(temp_in_path)
                    if os.path.exists(temp_out_path): os.remove(temp_out_path)

    st.success("¡Todos los archivos han sido procesados!")