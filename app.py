# Aplicación web para descargar videos de YouTube en formato mp3 o mp4 

import streamlit as st
import os


if ["yt-url"] not in st.session_state:
    st.session_state["yt-url"] = ""

def download(ydl_opts, url, filename):
    import yt_dlp as ydl

    try:
        with ydl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        with open(filename, "rb") as f:
            st.success("✅ Download completed")
            st.download_button("📥 Download file", f, file_name=filename)
        os.remove(filename)

    except Exception as ex:
        st.error(f"Error: {ex}")

def page1():
    main_container = st.container()
    url_form = st.form(key="url-form", clear_on_submit=True, enter_to_submit=True)

    with main_container:    
        st.header("YouTube Video Converter & Downloader")
        with url_form:
            txt_input = st.text_input("Enter the video URL from YouTube", key="input-url")
            formato = st.radio("Choose format", ["MP4 (Video)", "MP3 (Audio)"], key="format")
            submitted = st.form_submit_button("Convert")

            if submitted and txt_input:
                st.session_state["yt-url"] = st.session_state["input-url"]

    if "yt-url" in st.session_state:
        url = st.session_state["yt-url"]
        dl_format = st.session_state["format"]

        st.info("⏳ Processing download, please wait...")
        
        if dl_format == "MP4 (Video)":
            ydl_opts = {
                "outtmpl": "video.mp4",
                "format": "bestvideo+bestaudio/best",
                "merge_output_format": "mp4"
            }
            filename = "video.mp4"
        else:
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": "audio.%(ext)s",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
            }
            filename = "audio.mp3"
        
        download(ydl_opts, url, filename)

        


page1()