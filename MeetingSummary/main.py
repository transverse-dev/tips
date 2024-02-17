
import numpy as np
import time
from transformers import pipeline
from .GPT import GPT

class MeetingSummary:
    """
    회의 내용을 요약해주는 Class입니다.
    args:
        _txt_history : 전체 회의 내용
        summary_txt : 현재 회의 요약 내용 (화면 표출) = GPT
        translated_txt : 현재 회의 변환 내용 = STT
        stream : 현재 쌓이고 있는 chunk들의 집합
        sr : sound rate
    """
    def __init__(self):
        # STT model instance
        self.transcriber = pipeline("automatic-speech-recognition", 
                                    model="openai/whisper-small") 
                                    # openai/whisper-large - RAM 용량 이슈 (10GB)
                                    # openai/whisper-small - 노트북 기준 적정 (1GB)
                                    # openai/whisper-jax - 속도 업그레이드? 연구 필요

        # GPT model instance
        self.GPT = GPT()
        # args
        self.summarized_txt = "summarized_txt"
        self.translated_txt = "translated_txt"
        self.stream = None
        self.sr = None
        self.timer_start = None

    def chunk_processing(self, y):
        y = y.astype(np.float32)
        y = y /np.max(np.abs(y))
        return y

    def summary(self):
        print("summary started")
        # STT
        try:
            print(len(self.stream)/self.sr, '초')
            self.translated_txt = self.transcriber({"sampling_rate": self.sr, "raw": self.stream})["text"]
            print(self.translated_txt)
            self.stream = None
            print("STT done")
        except:
            print("STT Errored")

        # LLM
        try:
            self.summarized_txt = self.GPT.askGPT(self.translated_txt)
            print("LLM done: ", self.summarized_txt)
        except: 
            print("LLM Errored")

    def recording(self, sr, new_chunk):
        y = self.chunk_processing(new_chunk)
        
        # 말 단위 조합해서 문장 만들기
        if self.stream is not None:
            self.stream = np.concatenate([self.stream, y])
        else:
            self.timer_start = int(time.time()) # 초시계 Start
            self.stream = y

        elapsed_time = int(time.time()) - self.timer_start
        if elapsed_time > 40:
            self.sr = sr * 2 # 왜인지 모르겠지만 sound_rate가 반으로 떨어져서 나와서 임의 조정.
            self.timer_start = int(time.time())
            return True
        else:
            return False