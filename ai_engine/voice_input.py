import subprocess
import shutil
import tempfile
import os


class VoiceDependencyError(RuntimeError):
    pass


def _check_dependency(cmd: str):
    if shutil.which(cmd) is None:
        raise VoiceDependencyError(
            f"Required dependency '{cmd}' not found in system PATH."
        )


def record_and_transcribe(duration: int = 20) -> str:
    """
    Records audio from the microphone and transcribes it using Whisper.
    Returns transcribed text.
    Raises VoiceDependencyError on missing tools.
    """

    # ---- Validate dependencies ----
    _check_dependency("ffmpeg")
    _check_dependency("whisper")

    with tempfile.TemporaryDirectory() as tmp:
        audio_path = os.path.join(tmp, "input.wav")

        # ---- Windows microphone capture (default device) ----
        ffmpeg_cmd = [
            "ffmpeg",
            "-y",
            "-f",
            "dshow",
            "-i",
            "audio=default",
            "-t",
            str(duration),
            audio_path,
        ]

        try:
            subprocess.run(
                ffmpeg_cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
        except subprocess.CalledProcessError:
            raise VoiceDependencyError(
                "Audio recording failed. Check microphone permissions."
            )

        # ---- Transcribe ----
        result = subprocess.run(
            [
                "whisper",
                audio_path,
                "--model",
                "base",
                "--language",
                "en",
                "--fp16",
                "False",
            ],
            capture_output=True,
            text=True,
        )

        if not result.stdout.strip():
            raise VoiceDependencyError("Whisper produced empty transcription.")

        return result.stdout.strip()
