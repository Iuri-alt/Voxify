import os
import time
import tempfile
import subprocess
import azure.cognitiveservices.speech as speechsdk
from fastapi import UploadFile
from app.config import AZURE_SPEECH_KEY, AZURE_SPEECH_REGION


def _converter_para_wav(caminho_origem: str) -> str:
    caminho_wav = f"{caminho_origem}.wav"
    try:
        subprocess.run(
            [
                "ffmpeg", "-y", "-i", caminho_origem,
                "-ac", "1", "-ar", "16000", "-sample_fmt", "s16",
                caminho_wav,
            ],
            check=True,
            capture_output=True,
        )
    except FileNotFoundError as error:
        raise RuntimeError("ffmpeg não encontrado no servidor.") from error
    except subprocess.CalledProcessError as error:
        raise RuntimeError(
            f"Falha ao converter áudio: {error.stderr.decode(errors='ignore')}"
        ) from error
    return caminho_wav


def transcrever_audio(arquivo: UploadFile) -> str:
    extensao = os.path.splitext(arquivo.filename or ".mp3")[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=extensao) as temp:
        temp.write(arquivo.file.read())
        caminho_original = temp.name

    caminho_wav = None
    try:
        caminho_wav = _converter_para_wav(caminho_original)

        speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
        speech_config.speech_recognition_language = "pt-BR"

        audio_config = speechsdk.audio.AudioConfig(filename=caminho_wav)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        
        texto_completo = []
        done = False

        def recognized_handler(evt):
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                if evt.result.text:
                    texto_completo.append(evt.result.text)

        def stop_handler(evt):
            nonlocal done
            done = True

        speech_recognizer.recognized.connect(recognized_handler)
        speech_recognizer.session_stopped.connect(stop_handler)
        speech_recognizer.canceled.connect(stop_handler)

        speech_recognizer.start_continuous_recognition()
        
        # Aguarda a conclusão da transcrição contínua
        while not done:
            time.sleep(0.2)
            
        speech_recognizer.stop_continuous_recognition()
        return " ".join(texto_completo).strip()

    finally:
        for caminho in (caminho_original, caminho_wav):
            if not caminho:
                continue
            try:
                os.remove(caminho)
            except OSError:
                pass