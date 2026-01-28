import sounddevice as sd
from scipy.io.wavfile import write
from pathlib import Path


def record_voice(filename="voice_note.wav", duration=15, sample_rate=44100):
    """
    Records voice input from microphone and saves to a WAV file.
    """
    print(f"\n🎙️ Recording for {duration} seconds... Speak now.")

    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()

    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    write(filename, sample_rate, recording)

    print("✅ Recording saved.")
    return filename
