
import numpy as np
from transformers import pipeline
from .GPT import askGPT

class MeetingSummary:
    """
    회의 내용을 요약해주는 객체입니다.
    args:
        _txt_history : 전체 회의 내용
        summary_txt : 현재 회의 *요약* 내용 (화면 표출) = GPT
        translated_txt : 현재 회의 *변환* 내용 = STT
        stream : 현재 쌓이고 있는 chunk들의 집합
        sr : sound rate
    """
    def __init__(self):
        # STT model instance
        self.transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-large-v2")
        # args
        self._txt_history = []
        self.summarized_txt = "Recording"
        self.translated_txt = "Recording"
        self.stream = None
        self.sr = None

    def STT(self):
        self.translated_txt = self.transcriber({"sampling_rate": self.sr, "raw": self.stream})["text"]
        self._txt_history.append(self.translated_txt)
    
    def chunk_processing(y):
        y = y.astype(np.float32)
        y /= np.max(np.abs(y))    
        return y

    def LLM(self):
        self.summarized_txt = askGPT(self.translated_txt, 
                                     self._txt_history)

    def summary(self):
        self.STT()
        self.LLM()
    
    def recording(self, sr, new_chunk):
        self.sr = sr
        y = self.chunk_processing(new_chunk)
        
        # 말 단위 조합해서 문장 만들기
        if self.stream is not None:
            self.stream = np.concatenate([self.stream, y])
        else:
            self.stream = y

        # n초마다 타이머 실행
        if len(self.stream) % 100 == 0:
            print('y: ', y)
            print("stream:", len(self.stream), self.stream)
        if len(self.stream) >= 2000: # chunk n개마다 요약
            return True     #recording 반환 값이 True면 summary 실행
        else:
            return False    #recording 반환 값이 False면 Pass
        

##### chunk Timer 도달 시 chunk recording 멈춤 현상 해결 필요


#######################
# Class 변환 이전 코드 #
#######################
# def STTandGPT(sr, stream):
#     # stt 실행
#     stt = transcribe(sr, stream)
#     TEXT_HISTORY.append(stt)
#     summary = GPTf(stt, TEXT_HISTORY)

#     print("stt 실행: ", len(stream))
#     print(stt)              ## STT 성능 확인용
#     return None, summary
    

# def summarySpeech(stream, new_chunk):
#     global summary

#     # 청크 소리파형 전처리
#     sr, y = chunk_processing(new_chunk)

#     # 말 단위 조합해서 문장 만들기
#     if stream is not None:
#         stream = np.concatenate([stream, y])
#     else:
#         stream = y

#     print(len(stream))

#     if len(stream) >= 2400000: #24000Hz * 100
#         # 5초마다 타이머 실행
#         stream, summary = STTandGPT(sr, stream)

#     return stream, summary