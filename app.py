import streamlit as st
import whisper
import os
import subprocess
from pathlib import Path
from datetime import datetime
  
# Set folders
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)
Path(OUTPUT_FOLDER).mkdir(exist_ok=True)

st.title("🎬 CAPTION SHARK")

uploaded_file = st.file_uploader("Upload your video (.mp4)", type=["mp4"])
style = st.selectbox("Choose caption style", ["Classic"])  # Style support coming later

if uploaded_file:
    video_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())
    st.success("✅ Video uploaded successfully!")

    st.write("Transcribing video...")
    model = whisper.load_model("base")
    result = model.transcribe(video_path)

    st.success("✅ Captions generated!")

    # Save subtitles
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    srt_filename = f"subtitles_{timestamp}.srt"
    srt_path = os.path.join(OUTPUT_FOLDER, srt_filename)

    with open(srt_path, "w", encoding="utf-8") as srt_file:
        for i, segment in enumerate(result["segments"], start=1):
            start = segment["start"]
            end = segment["end"]
            text = segment["text"].strip()

            # Format time
            def format_time(seconds):
                ms = int((seconds % 1) * 1000)
                h = int(seconds // 3600)
                m = int((seconds % 3600) // 60)
                s = int(seconds % 60)
                return f"{h:02}:{m:02}:{s:02},{ms:03}"

            srt_file.write(f"{i}\n")
            srt_file.write(f"{format_time(start)} --> {format_time(end)}\n")
            srt_file.write(f"{text}\n\n")

    # FFmpeg burn-in
    output_video_path = os.path.join(OUTPUT_FOLDER, "captioned_video.mp4")

    # Convert paths for FFmpeg
    srt_ffmpeg_path = srt_path.replace("\\", "/")
    video_ffmpeg_path = video_path.replace("\\", "/")
    output_ffmpeg_path = output_video_path.replace("\\", "/")

    st.write("Burning captions into video...")

    # Command
    command = [
        "ffmpeg", "-y", "-i", video_ffmpeg_path,
        "-vf", f"subtitles='{srt_ffmpeg_path}'",
        output_ffmpeg_path
    ]

    # Optional debug info
    st.code(" ".join(command))

    try:
        subprocess.run(command, check=True)
        st.success("✅ Captioned video created!")
        with open(output_video_path, "rb") as f:
            st.download_button("📥 Download Captioned Video", f, file_name="captioned_video.mp4")
    except subprocess.CalledProcessError as e:
        st.error("❌ FFmpeg failed to generate the captioned video.")
        st.text(e)
