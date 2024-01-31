import os
from openai import OpenAI
import tiktoken

## OpenAI API 키 설정 -> 환경변수로 OPENAI_API_KEY 설정 or 메모장에 작성
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# models
EMBEDDING_MODEL = "text-embedding-ada-002"
GPT_MODEL = "gpt-3.5-turbo"


def num_tokens(text: str, model: str = GPT_MODEL) -> int:
    # 문자열 토큰 수 반환
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def get_history_messages(
        text_history: list,
        history_token_budget: int
) -> str:
    # 토큰 제한 안에서 history 최신 순으로 가져옴
    selected_text_history = ""
    for conversation in text_history[::-1]:
        next_conv = f"{conversation}\n"
        if num_tokens(selected_text_history + next_conv) < history_token_budget:
            selected_text_history += next_conv
        else:
            break
    return selected_text_history

def askGPT(
        query: str,
        text_history: list,
        model: str = GPT_MODEL,
        token_budget: int = 4096 - 1000,
) -> object:

    # 데이터프레임과 임베딩을 활용해 GPT로 쿼리 응답 반환
    selected_text_history = get_history_messages(
        text_history=text_history,
        history_token_budget=token_budget - 500
    )

    gpt_messages = [
        {"role": "system", "content": "회의 내용을 한국어로 요약하는 서기 챗봇입니다. 회의내용 텍스트가 정확하지 않을 수 있습니다. 회의내용을 유추하여 현재 회의내용을 요약하세요."},
        {"role": 'assistant', 'content': '이전 회의내용: ' + selected_text_history},
        {"role": "user", "content": "현재 회의내용: " + query}
    ]

    client = OpenAI(api_key=OPENAI_API_KEY)

    chatbot_response = client.chat.completions.create(
        model=model, 
        messages=gpt_messages,
        temperature=0)

    # print(chatbot_response)

    return chatbot_response.choices[0].message.content