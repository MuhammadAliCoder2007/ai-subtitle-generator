import whisper
import imageio_ffmpeg
import os
import warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")
 
# Get the base path (directory of the current script)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load Whisper model
model = whisper.load_model("base")

# Path to the uploaded video
video_path = BASE_DIR + "\\uploads\\video.mp4"

print("video_path: {0}", video_path)

# Transcribe the video
result = model.transcribe(video_path)

# Print full transcript
print("\n📝 Full Transcript:")
print(result["text"])

# Print segments with timestamps
print("\n📍 Segments:")
for segment in result["segments"]:
    print(f"[{segment['start']:.2f}s - {segment['end']:.2f}s] {segment['text']}")
