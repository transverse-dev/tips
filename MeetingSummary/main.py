import torch
import numpy as np
import time
from transformers import pipeline
from .GPT import GPT

class MeetingSummary:
    """
    회의 내용을 요약해주는 객체입니다.
    args:
        _txt_history : 전체 회의 내용
        summary_txt : 현재 회의 요약 내용 (화면 표출) = GPT
        translated_txt : 현재 회의 변환 내용 = STT
        stream : 현재 쌓이고 있는 chunk들의 집합
        sr : sound rate
    """
    def __init__(self):
        # STT model instance
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.transcriber = pipeline("automatic-speech-recognition", 
                                    model="openai/whisper-large-v2",
                                    chunk_length_s=30,
                                    device=device)
        # GPT model instance
        self.GPT = GPT()
        # args
        self.summarized_txt = "Recording"
        self.translated_txt = "Recording"
        self.stream = None
        self.sr = None
        self.timer_start = None
    
    def chunk_processing(y):
        y = y.astype(np.float32)
        y /= np.max(np.abs(y))    
        return y

    def summary(self):
        # STT
        self.translated_txt = self.transcriber({"sampling_rate": self.sr, "raw": self.stream}
                                               , batch_size=8)["text"]
        self.stream = None
        # LLM
        self.summarized_txt = self.GPT.askGPT(self.translated_txt)
    
    def recording(self, sr, new_chunk):
        self.sr = sr
        y = self.chunk_processing(new_chunk)
        
        # 말 단위 조합해서 문장 만들기
        if self.stream is not None:
            # self.stream = np.concatenate([self.stream, y])
            pass
        else:
            self.timer_start = time.time() # 초시계 Start
            self.stream = y

        elapsed_time = time.time() - self.timer_start
        if elapsed_time >= 40:
            return True
        else:
            return False


        # if len(self.stream) % 100 == 0:
        #     print('y: ', y)
        #     print("stream:", len(self.stream), self.stream)
        # if len(self.stream) >= 2000: # chunk n개마다 요약
        #     return True     #recording 반환 값이 True면 summary 실행
        # else:
            # return False    #recording 반환 값이 False면 Pass