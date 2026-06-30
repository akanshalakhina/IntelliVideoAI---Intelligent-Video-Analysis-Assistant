import yt_dlp
import subprocess
import os
import glob

DOWNLOAD_DIR = 'downloades'
os.makedirs(DOWNLOAD_DIR,exist_ok = True)

def download_youtube_audio(url :str) ->str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")
    return filename



def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to WAV using FFmpeg."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"

    command = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-ac", "1",        # Mono
        "-ar", "16000",    # 16 kHz
        output_path
    ]

    subprocess.run(command, check=True)

    return output_path

def chunk_audio(wav_path: str, chunk_minutes: int = 10) -> list:
    """Split WAV into 10-minute chunks using FFmpeg."""

    chunk_seconds = chunk_minutes * 60
    output_pattern = wav_path.replace(".wav", "_chunk_%03d.wav")

    command = [
        "ffmpeg",
        "-y",
        "-i", wav_path,
        "-f", "segment",
        "-segment_time", str(chunk_seconds),
        "-c", "copy",
        output_pattern
    ]

    subprocess.run(command, check=True)

    chunks = sorted(glob.glob(wav_path.replace(".wav", "_chunk_*.wav")))

    return chunks
    return chunks

def process_input(source: str) -> list:
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks

