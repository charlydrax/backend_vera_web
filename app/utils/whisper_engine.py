# import whisper

# model = whisper.load_model("base")

# def transcribe_audio(audio_path):
#     result = model.transcribe(audio_path)
#     return result["text"]

def transcribe_audio(file_path: str) -> str:
    """
    Transcrit un fichier audio en texte avec Whisper.
    """
    # result = model.transcribe(file_path)
    # return result.get("text", "")
    return " Indisponible "
