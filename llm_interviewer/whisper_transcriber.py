from faster_whisper import WhisperModel

model = WhisperModel("base")  # Use 'tiny', 'base', etc. based on your system resources

def transcribe_audio(audio_path):
    if audio_path is None:
        return ""
    segments, _ = model.transcribe(audio_path)
    text = " ".join(segment.text for segment in segments)
    return text.strip()
