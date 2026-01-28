from faster_whisper import WhisperModel


model = WhisperModel("base", compute_type="int8")


def transcribe_audio(audio_path: str) -> str:
    """
    Converts spoken audio into text using Whisper.
    """
    segments, _ = model.transcribe(audio_path)

    text = ""
    for segment in segments:
        text += segment.text + " "

    return text.strip()
