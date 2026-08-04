# Aplicación web para descargar videos de YouTube en formato mp3 o mp4
import streamlit as st
import glob
import io
import os

if "yt-url" not in st.session_state:
    st.session_state["yt-url"] = ""

st.set_page_config(
    page_title="YT Converter",
    page_icon="▶",
    layout="centered",
)

DARK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=IBM+Plex+Mono:wght@300;400&display=swap');

/* ── Global ── */
html, body, .stApp {
    background: #080808 !important;
    color: #c8c8c8 !important;
    font-family: 'IBM Plex Mono', monospace !important;
}

/* Barra roja superior */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: #e02020;
    z-index: 9999;
}

/* ── Ocultar chrome de Streamlit ── */
#MainMenu, footer,
header[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] {
    display: none !important;
}

/* ── Layout ── */
.main .block-container {
    max-width: 560px !important;
    padding: 5rem 1.75rem 3rem !important;
}

/* ── Card del formulario ── */
[data-testid="stForm"] {
    background: #0e0e0e !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 8px !important;
    padding: 1.5rem 1.75rem 1.75rem !important;
}

/* ── Labels de widgets ── */
.stRadio > label,
.stSelectbox > label,
[data-testid="stWidgetLabel"] > p,
label[for] {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.63rem !important;
    font-weight: 400 !important;
    color: #707070 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.14em !important;
}

/* ── Label "Video URL" destacado ── */
.stTextInput label {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    color: #e02020 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.14em !important;
}

/* ── Rueda de carga junto al input ── */
.ytc-spinner-wrap {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    height: 100%;
    padding-bottom: 0.1rem;
}
.ytc-spinner {
    width: 20px;
    height: 20px;
    border: 2px solid rgba(224,32,32,0.15);
    border-top-color: #e02020;
    border-radius: 50%;
    animation: ytc-spin 0.7s linear infinite;
}
@keyframes ytc-spin {
    to { transform: rotate(360deg); }
}

/* ── Text Input ── */
.stTextInput input {
    background: #080808 !important;
    border: 1px solid #1e1e1e !important;
    border-radius: 4px !important;
    color: #e0e0e0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.8rem !important;
    padding: 0.65rem 0.9rem !important;
    transition: border-color 0.12s !important;
    caret-color: #e02020 !important;
}
.stTextInput input:focus {
    border-color: #e02020 !important;
    box-shadow: 0 0 0 1px rgba(224,32,32,0.3) !important;
    outline: none !important;
    background: #0a0a0a !important;
}
.stTextInput input::placeholder { color: #252525 !important; }

/* Oculta el "Press Enter to submit form" que Streamlit añade al input */
.stTextInput [data-testid="InputInstructions"],
.stTextInput [data-testid="stWidgetInstructions"],
[data-testid="InputInstructions"],
[data-testid="stWidgetInstructions"] {
    display: none !important;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: #080808 !important;
    border: 1px solid #1e1e1e !important;
    border-radius: 4px !important;
    color: #e0e0e0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.8rem !important;
}
[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within {
    border-color: #e02020 !important;
    box-shadow: 0 0 0 1px rgba(224,32,32,0.3) !important;
}
[data-testid="stSelectbox"] svg { fill: #2a2a2a !important; }
[data-testid="stSelectbox"] ul {
    background: #0e0e0e !important;
    border: 1px solid #1e1e1e !important;
    border-radius: 4px !important;
}
[data-testid="stSelectbox"] li {
    background: transparent !important;
    color: #b0b0b0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.78rem !important;
}
[data-testid="stSelectbox"] li:hover,
[data-testid="stSelectbox"] li[aria-selected="true"] {
    background: rgba(224,32,32,0.1) !important;
    color: #e0e0e0 !important;
}

/* ── Radio ── */
[data-testid="stRadio"] > div {
    flex-direction: row !important;
    gap: 0.5rem !important;
    flex-wrap: wrap !important;
}
[data-testid="stRadio"] label {
    background: #080808 !important;
    border: 1px solid #1a1a1a !important;
    border-radius: 4px !important;
    padding: 0.35rem 0.85rem !important;
    transition: border-color 0.12s !important;
    cursor: pointer !important;
}
[data-testid="stRadio"] label:hover { border-color: #333 !important; }

/* ── Botones del formulario (base común) ── */
[data-testid="stFormSubmitButton"] button {
    border-radius: 4px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.73rem !important;
    letter-spacing: 0.22em !important;
    text-transform: uppercase !important;
    padding: 0.7rem 1rem !important;
    width: 100% !important;
    transition: background 0.12s, border-color 0.12s, color 0.12s, transform 0.08s !important;
    cursor: pointer !important;
}

/* ── Botón Convert (primario) ── */
[data-testid="stBaseButton-primaryFormSubmit"] {
    background: #e02020 !important;
    color: #ffffff !important;
    border: 1px solid #e02020 !important;
}
[data-testid="stBaseButton-primaryFormSubmit"]:hover {
    background: #c91818 !important;
    border-color: #c91818 !important;
    transform: translateY(-1px) !important;
}
[data-testid="stBaseButton-primaryFormSubmit"]:active {
    transform: translateY(0) !important;
    background: #b01010 !important;
}

/* ── Botón Clear (secundario) ── */
[data-testid="stBaseButton-secondaryFormSubmit"] {
    background: transparent !important;
    color: #707070 !important;
    border: 1px solid #222 !important;
}
[data-testid="stBaseButton-secondaryFormSubmit"]:hover {
    border-color: #e02020 !important;
    color: #e02020 !important;
    background: rgba(224,32,32,0.04) !important;
    transform: translateY(-1px) !important;
}
[data-testid="stBaseButton-secondaryFormSubmit"]:active {
    transform: translateY(0) !important;
    background: rgba(224,32,32,0.09) !important;
}

/* ── Botón Descargar ── */
.stDownloadButton button {
    background: transparent !important;
    color: #c0c0c0 !important;
    border: 1px solid #222 !important;
    border-radius: 4px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.65rem 1.5rem !important;
    width: 100% !important;
    transition: all 0.12s !important;
    margin-top: 0.5rem !important;
}
.stDownloadButton button:hover {
    border-color: #e02020 !important;
    color: #e02020 !important;
    background: rgba(224,32,32,0.04) !important;
}

/* ── Alertas ── */
.stAlert, [data-testid="stAlert"],
div[data-testid="stAlert"] {
    background: #0e0e0e !important;
    border: 1px solid #1a1a1a !important;
    border-radius: 4px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.75rem !important;
    color: #888 !important;
    padding: 0.75rem 1rem !important;
}
.stSuccess, [data-testid="stAlert"][data-baseweb="notification"] {
    border-color: rgba(0,180,80,0.2) !important;
    color: #009944 !important;
}
.stError { border-color: rgba(224,32,32,0.3) !important; color: #c03030 !important; }

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #0a0a0a !important;
    border: 1px solid #141414 !important;
    border-radius: 4px !important;
    margin-top: 1.5rem !important;
}
[data-testid="stExpander"] summary,
.streamlit-expanderHeader {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.63rem !important;
    color: #606060 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.14em !important;
    padding: 0.75rem 1rem !important;
}
[data-testid="stExpander"] summary:hover { color: #909090 !important; }

/* ── Imagen thumbnail (centrada, estilo YouTube) ── */
.stImage {
    display: flex !important;
    justify-content: center !important;
}
.stImage img {
    border-radius: 8px !important;
    border: 1px solid #1a1a1a !important;
    width: 100% !important;
    aspect-ratio: 16 / 9 !important;
    object-fit: cover !important;
}

/* ── Subheader (título encima del thumbnail, centrado) ── */
h3 {
    font-family: 'Syne', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    color: #e0e0e0 !important;
    letter-spacing: -0.01em !important;
    margin: 0.75rem 0 0.6rem !important;
    text-align: center !important;
}

/* ── Menú de autenticación (popover arriba a la derecha) ── */
[data-testid="stPopover"] {
    display: flex !important;
    justify-content: flex-end !important;
}
[data-testid="stPopoverButton"] {
    background: #0e0e0e !important;
    border: 1px solid #1a1a1a !important;
    border-radius: 999px !important;
    color: #909090 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.06em !important;
    padding: 0.4rem 0.75rem !important;
    transition: border-color 0.12s, color 0.12s !important;
}
[data-testid="stPopoverButton"]:hover {
    border-color: #e02020 !important;
    color: #e02020 !important;
}
[data-testid="stPopoverBody"] {
    background: #0e0e0e !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 8px !important;
    padding: 1rem 1.1rem !important;
}

/* ── Markdown ── */
.stMarkdown p, .stMarkdown li {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.73rem !important;
    color: #666 !important;
    line-height: 1.9 !important;
}
.stMarkdown a { color: #e02020 !important; text-decoration: none !important; }
.stMarkdown a:hover { text-decoration: underline !important; }
.stMarkdown code {
    background: #111 !important;
    color: #666 !important;
    font-size: 0.72rem !important;
    padding: 0.1em 0.4em !important;
    border-radius: 2px !important;
    border: 1px solid #1e1e1e !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: #080808; }
::-webkit-scrollbar-thumb { background: #1e1e1e; border-radius: 2px; }

/* ── Selección de texto ── */
::selection { background: rgba(224,32,32,0.22); color: #f0f0f0; }
</style>
"""

HEADER_HTML = """
<div style="margin-bottom:2.25rem;">
    <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.35rem;">
        <div style="
            width:22px;height:22px;
            background:#e02020;
            border-radius:3px;
            display:flex;align-items:center;justify-content:center;
            flex-shrink:0;
        ">
            <svg width="8" height="10" viewBox="0 0 8 10" fill="none">
                <path d="M0.5 1L7.5 5L0.5 9V1Z" fill="white"/>
            </svg>
        </div>
        <span style="
            font-family:'Syne',sans-serif;
            font-size:1.3rem;
            font-weight:800;
            color:#f0f0f0;
            letter-spacing:-0.03em;
            line-height:1;
        ">YT Converter</span>
    </div>
    <p style="
        font-family:'IBM Plex Mono',monospace;
        font-size:0.6rem;
        color:#484848;
        margin:0;
        letter-spacing:0.16em;
        text-transform:uppercase;
    ">Audio &amp; Video Download</p>
</div>
"""


FORMAT_OPTIONS = ["MP3 (Audio)", "MP4 (Video)"]
QUALITY_OPTIONS = ["best (max available)", "1080p", "720p", "480p", "360p"]


def format_file_size(num_bytes):
    size = float(num_bytes)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.1f} {unit}" if unit != "B" else f"{int(size)} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def embed_square_cover(mp3_path, thumb_path):
    from PIL import Image
    from mutagen.id3 import ID3, APIC, ID3NoHeaderError

    with Image.open(thumb_path) as img:
        side = min(img.size)
        left = (img.width - side) // 2
        top = (img.height - side) // 2
        square = img.convert("RGB").crop((left, top, left + side, top + side))
        cover = io.BytesIO()
        square.save(cover, format="JPEG", quality=90)

    try:
        tags = ID3(mp3_path)
    except ID3NoHeaderError:
        tags = ID3()
    tags.delall("APIC")
    tags.add(APIC(encoding=0, mime="image/jpeg", type=3, desc="Cover", data=cover.getvalue()))
    tags.save(mp3_path)


def download(ydl_opts, url, filename):
    import yt_dlp as ydl

    def clean_url_list(raw_url: str):
        if not raw_url:
            return ""
        if raw_url.startswith('https://youtu.be/'): 
            url_sin_list = raw_url.split('?list')
        else: 
            url_sin_list = raw_url.split('&list')
        return url_sin_list[0]

    try:
        with ydl.YoutubeDL(ydl_opts) as ydl_:
            clean_url = clean_url_list(url)
            info_dict = ydl_.extract_info(clean_url, download=True)
            thumbnail_url = info_dict.get("thumbnail", None)
            title = info_dict.get("title", "Unknown Title")
            filename = title + (".mp4" if filename.endswith(".mp4") else ".mp3")
            return {"filename": filename, "title": title, "thumbnail_url": thumbnail_url}
    except Exception as ex:
        st.error(f"Error: {ex}")
        return None


def clear_form():
    # Se ejecuta como callback del submit, antes del rerun, así que sí puede
    # reescribir el estado de widgets ya instanciados en el run anterior.
    st.session_state["input-url"] = ""
    st.session_state["yt-url"] = ""
    st.session_state["format"] = FORMAT_OPTIONS[0]
    st.session_state["quality"] = QUALITY_OPTIONS[0]


def yt_downloader():
    st.markdown(DARK_CSS, unsafe_allow_html=True)

    main_container = st.container()
    url_form = st.form(key="url-form", clear_on_submit=False, enter_to_submit=True)

    with main_container:
        header_col, auth_col = st.columns([5, 1.4], vertical_alignment="center")

        with header_col:
            st.markdown(HEADER_HTML, unsafe_allow_html=True)

        with auth_col:
            # ── Autenticación (fuera del form porque file_uploader no funciona dentro) ──
            with st.popover("🔐 Auth", use_container_width=True):
                cookie_method = st.radio(
                    "Method",
                    ["None", "From browser", "From file"],
                    key="cookie_method",
                    horizontal=True,
                )
                if cookie_method == "From browser":
                    st.selectbox(
                        "Browser",
                        ["chrome", "firefox", "edge", "brave", "chromium", "opera", "vivaldi", "safari"],
                        key="cookie_browser",
                    )
                    st.caption("Reads cookies from the browser profile on this machine.")
                elif cookie_method == "From file":
                    uploaded = st.file_uploader(
                        "cookies.txt",
                        type=["txt"],
                        key="cookie_upload",
                        help="Export with a browser extension like 'Get cookies.txt LOCALLY'",
                    )
                    if uploaded is not None:
                        st.session_state["cookie_file_bytes"] = uploaded.read()

        with url_form:
            input_col, spinner_col = st.columns([5, 1], vertical_alignment="bottom")
            with input_col:
                txt_input = st.text_input(
                    "Video URL",
                    placeholder="https://youtube.com/watch?v=...",
                    key="input-url",
                )
            with spinner_col:
                spinner_slot = st.empty()
            format_col, quality_col = st.columns(2)
            with format_col:
                formato = st.radio("Format", FORMAT_OPTIONS, key="format", horizontal=True)
            with quality_col:
                calidad = st.selectbox("Quality", QUALITY_OPTIONS, key="quality")

            _, clear_col, button_col = st.columns([1.6, 1, 1])
            with clear_col:
                st.form_submit_button(
                    "Clear",
                    on_click=clear_form,
                    use_container_width=True,
                )
            with button_col:
                submitted = st.form_submit_button(
                    "Convert",
                    type="primary",
                    use_container_width=True,
                )

            if submitted and txt_input:
                st.session_state["yt-url"] = st.session_state["input-url"]

        if st.session_state.get("yt-url"):
            url = st.session_state["yt-url"]
            dl_format = st.session_state["format"]

            # Restos de una descarga previa incompleta (p.ej. "audio.mp4.part") hacen que
            # yt-dlp intente reanudarla con un header Range que el servidor ya no acepta,
            # provocando "HTTP Error 416: Requested range not satisfiable".
            for stray in glob.glob("video.*") + glob.glob("audio.*"):
                try:
                    os.remove(stray)
                except OSError:
                    pass

            download_info = st.info("Processing...")
            spinner_slot.markdown(
                '<div class="ytc-spinner-wrap"><div class="ytc-spinner"></div></div>',
                unsafe_allow_html=True,
            )

            cookie_method = st.session_state.get("cookie_method", "None")

            # Opciones base: cliente android evita SABR/HLS y errores de firma del cliente web.
            # continuedl/overwrites en False/True fuerzan una descarga limpia en vez de intentar
            # reanudar un archivo parcial (fuente del error 416).
            base_opts = {
                "extractor_args": {"youtube": {"player_client": ["android"]}},
                "retries": 6,
                "fragment_retries": 6,
                "continuedl": False,
                "overwrites": True,
                "http_headers": {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
                },
            }

            if dl_format == "MP4 (Video)":
                quality_map = {
                    "best (max available)": "bestvideo+bestaudio/best",
                    "1080p": "bestvideo[height<=1080]+bestaudio/best",
                    "720p": "bestvideo[height<=720]+bestaudio/best",
                    "480p": "bestvideo[height<=480]+bestaudio/best",
                    "360p": "bestvideo[height<=360]+bestaudio/best",
                }
                fmt = quality_map.get(st.session_state["quality"], "bestvideo+bestaudio/best")
                ydl_opts = {
                    **base_opts,
                    "outtmpl": "video.mp4",
                    "format": fmt,
                    "merge_output_format": "mp4",
                }
                filename = "video.mp4"
                mime_type = "video/mp4"
            else:
                ydl_opts = {
                    **base_opts,
                    "format": "bestaudio/best",
                    "outtmpl": "audio.%(ext)s",
                    # La miniatura se deja en disco (sin EmbedThumbnail) para recortarla
                    # a cuadrado e incrustarla después con embed_square_cover().
                    "writethumbnail": True,
                    "postprocessors": [
                        {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"},
                        {"key": "FFmpegMetadata"},
                    ],
                }
                filename = "audio.mp3"
                mime_type = "audio/mpeg"

            # Inyectar cookies según método elegido
            cookie_path = "/tmp/yt_cookies.txt"
            if cookie_method == "From browser":
                browser = st.session_state.get("cookie_browser", "chrome")
                ydl_opts["cookiesfrombrowser"] = (browser,)
            elif cookie_method == "From file":
                cookie_bytes = st.session_state.get("cookie_file_bytes")
                if cookie_bytes:
                    with open(cookie_path, "wb") as cf:
                        cf.write(cookie_bytes)
                    ydl_opts["cookiefile"] = cookie_path
                else:
                    st.warning("No cookies file loaded — proceeding without authentication.")

            result = download(ydl_opts, url, filename)
            download_info.empty()
            spinner_slot.empty()

            # Limpiar archivo de cookies temporal
            if cookie_method == "From file" and os.path.exists(cookie_path):
                os.remove(cookie_path)

            if result and os.path.exists(filename):
                # writethumbnail deja la miniatura junto al mp3 ("audio.webp"/"audio.jpg").
                for thumb in [p for p in glob.glob("audio.*") if p != filename]:
                    try:
                        if filename.endswith(".mp3"):
                            embed_square_cover(filename, thumb)
                    except Exception as ex:
                        st.warning(f"Could not embed cover art: {ex}")
                    finally:
                        try:
                            os.remove(thumb)
                        except OSError:
                            pass

                file_size = format_file_size(os.path.getsize(filename))

                st.subheader(result["title"])
                st.image(result["thumbnail_url"], width="stretch")
                st.success(f"Download complete — {file_size}")

                with open(filename, "rb") as f:
                    buffer = io.BytesIO(f.read())

                st.download_button(
                    f"↓  {result['filename']} ({file_size})",
                    data=buffer,
                    file_name=result["filename"],
                    mime=mime_type,
                )

                os.remove(filename)

    with st.expander("Supported URL formats"):
        st.markdown("""
- `https://www.youtube.com/watch?v=...`
- `https://youtu.be/...`
        """)


if __name__ == "__main__":
    yt_downloader()
