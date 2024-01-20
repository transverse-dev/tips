from transformers import pipeline
import numpy as np
from pydub import AudioSegment


def mp3ToWav(mp3):
    # convert mp3 file to wav                                                       
    # sound = AudioSegment.from_mp3("transcript.mp3")
    # sound.export("transcript.wav", format="wav")
    pass

def chunk_processing(new_chunk):
    sr, y = new_chunk
    y = y.astype(np.float32)
    y /= np.max(np.abs(y))    
    return sr, y

# openai whisper large 모델(6Gb) 사용시 노트북에 무리가 있음.
# openai whisper base 모델을 사용해서 테스트함.
# 국내 유료 STT 모델 API를 사용하면 성능 향상.
# whisper를 직접 fine tuning 하는 방법도 있음.
def transcribe(sr, stream):
    transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-large-v2")
    # transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-base")
    return transcriber({"sampling_rate": sr, "raw": stream})["text"]
