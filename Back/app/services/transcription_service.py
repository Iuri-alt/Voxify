import os
import time
import tempfile
import azure.cognitiveservices.speech as speechsdk
from fastapi import UploadFile
from app.config import AZURE_SPEECH_KEY, AZURE_SPEECH_REGION

def transcrever_audio(arquivo: UploadFile) -> str:
    extensao = os.path.splitext(arquivo.filename or ".mp3")[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=extensao) as temp:
        temp.write(arquivo.file.read())
        caminho = temp.name

    try:
        speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
        speech_config.speech_recognition_language = "pt-BR"
        
        audio_config = speechsdk.audio.AudioConfig(filename=caminho)
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
        try:
            os.remove(caminho)
        except OSError:
            pass