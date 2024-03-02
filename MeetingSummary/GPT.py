from os import getenv
from openai import OpenAI
from tiktoken import encoding_for_model


class GPT(object):
    def __init__(self):
        # OpenAI API 키 설정 -> 환경변수로 OPENAI_API_KEY 설정
        self.OPENAI_API_KEY = getenv('OPENAI_API_KEY')

        # models
        self.EMBEDDING_MODEL = "text-embedding-ada-002"
        self.GPT_MODEL = "gpt-3.5-turbo"

        # args
        self.token_budget = 4096 - 1024
        self.history_token_budget = None
        self.text_history = []
        self.query = None

    def num_tokens(self, query) -> int:
        # 문자열 토큰 수 반환
        encoding = encoding_for_model(self.GPT_MODEL)
        return len(encoding.encode(query))
    
    def get_history_messages(self) -> str:
        # 토큰 제한 안에서 history 최신 순으로 가져옴
        selected_text_history = ""
        for conversation in self.text_history[::-1]:
            next_conv = f"{conversation}\n"
            if self.num_tokens(selected_text_history + next_conv) < self.history_token_budget:
                selected_text_history += next_conv
            else:
                break
        return selected_text_history

    def askGPT(
        self,
        query: str
    ) -> str:
        
        # 질의 저장
        self.query = query
        self.history_token_budget = self.token_budget - self.num_tokens(query)

        # 데이터프레임과 임베딩을 활용해 GPT로 쿼리 응답 반환
        selected_text_history = self.get_history_messages()

        gpt_messages = [
            {"role": "system", "content": "회의 내용을 한국어로 요약하는 서기 챗봇입니다. 현재 회의내용을 정확하게 요약하세요."},
            {"role": 'assistant', 'content': '이전 회의내용: ' + selected_text_history},
            {"role": "user", "content": "현재 회의내용: " + query}
        ]

        client = OpenAI(api_key=self.OPENAI_API_KEY)

        chatbot_response = client.chat.completions.create(
            model=self.GPT_MODEL, 
            messages=gpt_messages,
            temperature=0)
        
        # text_history 저장
        self.text_history.append(query)

        return chatbot_response.choices[0].message.content
