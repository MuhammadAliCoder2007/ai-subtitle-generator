import whisper
import os

# Set base paths
video_path = "uploads/video.mp4"
srt_path = "output/subtitles.srt" 

# Make sure output folder exists
os.makedirs("output", exist_ok=True)

# Load Whisper model
model = whisper.load_model("base")
result = model.transcribe(video_path)

# Generate SRT content
def format_timestamp(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"

lines = []
for i, segment in enumerate(result["segments"], 1):
    start = format_timestamp(segment["start"])
    end = format_timestamp(segment["end"])
    text = segment["text"].strip()
    lines.append(f"{i}\n{start} --> {end}\n{text}\n")

# Write to .srt file
with open(srt_path, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("✅ SRT subtitles generated successfully!")
