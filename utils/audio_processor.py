import os
import yt_dlp
from pydub import AudioSegment

DOWNLOAD_DIR = os.getcwd()

def download_youtube_audio(url: str) -> str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": "192",
        }],
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    wav_file = os.path.splitext(filename)[0] + ".wav"

    if not os.path.exists(wav_file):
        raise FileNotFoundError(f"WAV file was not created: {wav_file}")

    return wav_file

    #yt-dlp  → Downloads
#FFmpeg → Converts
#Whisper → Listens
#Mistral → Thinks
def convert_audio_to_wav(input_path:str)->str:
    """"Convert any audio/video file to WAV format using pydub"""
    output_path = os.path.splitext(input_path)[0] + '.wav'
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000) # Convert to mono and set frame rate    
    audio.export(output_path, format='wav')
    return output_path



def chunk_audio(wav_path : str, chunk_minutes : int = 10) -> list:
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000  # Convert minutes to milliseconds
    chunks = []
    # 50 min video = 50*60*1000 = 3,000,000 ms 10 min chunks = 10*60*1000 = 600,000 ms then (0,3000000,600000)
    for i,start in enumerate(range(0, len(audio), chunk_ms)):
  
        chunk = audio[start:start + chunk_ms]
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path, format='wav')
        chunks.append(chunk_path)
    return chunks

def process_input(source:str)->list:
    if source.startswith('https://') or source.startswith('http://'):
       print(f"Downloading audio from YouTube URL: {source}")
       wav_path = download_youtube_audio(source)
        
    else:
        print("Detected local file. Converting to WAV format...")
        wav_path = convert_audio_to_wav(source)
    print("Splitting audio into chunks...")    
    chunks = chunk_audio(wav_path)
    print(f"Audio ready - {len(chunks)} chunks created.")
    return chunks

