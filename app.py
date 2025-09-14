# Aplicación web para descargar videos de YouTube en formato mp3 o mp4 
import streamlit as st
import io
import os

if "yt-url" not in st.session_state:
    st.session_state["yt-url"] = ""

st.set_page_config(
    page_title="YouTube Downloader",
    page_icon="https://cdn-icons-png.flaticon.com/512/1384/1384060.png",
    layout="centered",
)

def download(ydl_opts, url, filename):
    import yt_dlp as ydl

    try:
        with ydl.YoutubeDL(ydl_opts) as ydl_:
            info_dict = ydl_.extract_info(url, download=True)

            # Extraer miniatura y título
            thumbnail_url = info_dict.get("thumbnail", None)
            title = info_dict.get("title", "Unknown Title")
            filename = title + (".mp4" if filename.endswith(".mp4") else ".mp3")

            return {"filename": filename, "title": title, "thumbnail_url": thumbnail_url}
    except Exception as ex:
        st.error(f"Error: {ex}")
        return None


def yt_downloader():
    main_container = st.container()
    url_form = st.form(key="url-form", clear_on_submit=False, enter_to_submit=True)

    with main_container:    
        st.markdown(
            """
            <h1 style="display: flex; align-items: center; gap: 10px;">
                <img src="https://cdn-icons-png.flaticon.com/512/1384/1384060.png" width="40">
                YouTube Downloader
            </h1>
            """,
            unsafe_allow_html=True
        )
        st.write("")
        with url_form:
            txt_input = st.text_input("Enter the video URL from YouTube", key="input-url")
            formato = st.radio("Choose format", ["MP3 (Audio)", "MP4 (Video)"], key="format")
            calidad = st.selectbox(
                "Video quality",
                ["best (max available)", "1080p", "720p", "480p", "360p"],
                key="quality"
            )
            submitted = st.form_submit_button("Convert")

            if submitted and txt_input:
                st.session_state["yt-url"] = st.session_state["input-url"]

        if "yt-url" in st.session_state and st.session_state["yt-url"] != "":
            url = st.session_state["yt-url"]
            dl_format = st.session_state["format"]

            download_info = st.info("⏳ Processing download, please wait...")

            # Ajuste según formato
            if dl_format == "MP4 (Video)":
                if st.session_state["quality"] == "best (max available)":
                    fmt = "bestvideo+bestaudio/best"
                elif st.session_state["quality"] == "1080p":
                    fmt = "bestvideo[height<=1080]+bestaudio/best"
                elif st.session_state["quality"] == "720p":
                    fmt = "bestvideo[height<=720]+bestaudio/best"
                elif st.session_state["quality"] == "480p":
                    fmt = "bestvideo[height<=480]+bestaudio/best"
                else:
                    fmt = "bestvideo[height<=360]+bestaudio/best"

                ydl_opts = {
                    "outtmpl": "video.mp4",
                    "format": fmt,
                    "merge_output_format": "mp4",
                    "http_headers": {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                                    "Chrome/115.0 Safari/537.36"
                    }
                }
                filename = "video.mp4"
                mime_type = "video/mp4"

            else:  # MP3
                ydl_opts = {
                    "format": "bestaudio/best",
                    "outtmpl": "audio.%(ext)s",
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "192",
                        },
                        {"key": "FFmpegMetadata"},
                    ],
                    "http_headers": {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/115.0 Safari/537.36"
                }
                }
                filename = "audio.mp3"
                mime_type = "audio/mpeg"

            result = download(ydl_opts, url, filename)
            download_info.empty()

            if result and os.path.exists(filename):
                st.image(result["thumbnail_url"], width=300)
                st.subheader(result["title"])
                st.success("✅ Downloaded successfully!")

                # Pasar el archivo a buffer en memoria
                with open(filename, "rb") as f:
                    buffer = io.BytesIO(f.read())

                st.download_button(
                    f"📥 Descargar {result['filename']}",
                    data=buffer,
                    file_name=result["filename"],
                    mime=mime_type,
                )

                # Borrar archivo temporal del servidor
                os.remove(filename)

    # Ejemplo de URLs válidas
    with st.expander("URL Format Example"):
        st.write("You can enter URLs from the following sites:")
        st.markdown("""
        - https://www.youtube.com/watch?v=example
        - https://www.youtube.com/playlist?list=example
        """)

if __name__ == "__main__":
    yt_downloader()