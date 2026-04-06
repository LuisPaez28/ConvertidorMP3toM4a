import streamlit as st
import subprocess
import tempfile
import os

# Configuración básica de la página
st.set_page_config(page_title="Convertidor a MP3", page_icon="🎵")

st.title("🎵 Convertidor Universal a MP3")
st.write("Sube tus archivos de audio (`.m4a`) o video (`.mp4`) y extrae el audio en `.mp3` fácilmente.")

# Selector de archivos: ¡Ahora acepta mp4 también!
archivos_subidos = st.file_uploader(
    "Arrastra tus archivos aquí o haz clic para buscar", 
    type=["m4a", "mp4"], 
    accept_multiple_files=True
)

if archivos_subidos:
    st.markdown("---")
    st.write("### Progreso de conversión")
    
    for i, archivo in enumerate(archivos_subidos):
        # Obtener la extensión original (.m4a o .mp4) para manejarla dinámicamente
        ext_original = os.path.splitext(archivo.name)[1].lower()
        
        # Generar el nuevo nombre del archivo reemplazando su extensión original
        nombre_mp3 = archivo.name.lower().replace(ext_original, ".mp3")
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Un pequeño detalle visual: cambiar el icono si es video o audio
            icono = "🎬" if ext_original == ".mp4" else "🎧"
            st.write(f"{icono} **{archivo.name}**")
            
        with col2:
            with st.spinner("Procesando..."):
                try:
                    # 1. Crear archivos temporales asegurando que tengan la extensión original
                    with tempfile.NamedTemporaryFile(delete=False, suffix=ext_original) as temp_in:
                        temp_in.write(archivo.read())
                        temp_in_path = temp_in.name
                        
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_out:
                        temp_out_path = temp_out.name

                    # 2. Ejecutar FFmpeg (¡Convierte M4A o extrae audio de MP4 sin cambiar nada!)
                    comando = [
                        "ffmpeg", 
                        "-y",             
                        "-i", temp_in_path, 
                        "-b:a", "192k",   
                        temp_out_path     
                    ]
                    
                    subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

                    # 3. Leer el MP3 resultante
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
                    
                except subprocess.CalledProcessError:
                    st.error("Error en la conversión con FFmpeg.")
                except Exception as e:
                    st.error(f"Ocurrió un error: {e}")
                finally:
                    # 5. Limpiar los archivos temporales
                    if os.path.exists(temp_in_path): os.remove(temp_in_path)
                    if os.path.exists(temp_out_path): os.remove(temp_out_path)

    st.success("¡Todos los archivos han sido procesados!")