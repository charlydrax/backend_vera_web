import ffmpeg
import os
import subprocess
from .whisper_engine import transcribe_audio

def video_to_text(video_path):
    audio_path = "/tmp/audio.wav"

    # Extraire audio
    (
        ffmpeg
        .input(video_path)
        .output(audio_path, ac=1, ar="16000")
        .overwrite_output()
        .run()
    )

    # Transcrire audio
    text = transcribe_audio(audio_path)

    return text
