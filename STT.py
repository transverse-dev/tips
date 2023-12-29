from transformers import pipeline
import numpy as np
from pydub import AudioSegment


def mp3ToWav(mp3):
    # convert mp3 file to wav                                                       
    # sound = AudioSegment.from_mp3("transcript.mp3")
    # sound.export("transcript.wav", format="wav")
    pass

# openai whisper large 모델(6Gb) 사용.
# 국내 유료 STT 모델 API를 사용하면 성능 향상.
# whisper를 직접 fine tuning 하는 방법도 있음.
def STTf(audio):
    transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-large-v2")

    sr, y = audio
    y = y.astype(np.float32)
    y /= np.max(np.abs(y))

    return transcriber({"sampling_rate": sr, "raw": y})["text"]
