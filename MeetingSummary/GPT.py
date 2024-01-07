import os
from openai import OpenAI
import tiktoken

## OpenAI API 키 설정 -> 환경변수로 OPENAI_API_KEY 설정 or 메모장에 작성
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# f = open('openai_key.txt', 'r')
# KEY = f.readline()
# openai.api_key = KEY


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

###############################
### 회의내용 요약 필요시 추가 ###
###############################
# def get_summary_history(
#         history_list: list,
#         model: str = GPT_MODEL
# ) -> str:
#     if history_list == []:
#         return ""
#     gpt_messages = [
#         {'role': 'system', 'content': '사용자와 "assistant"의 모든 대화를 한 문단으로 요약하여 설명하는 "assistant"입니다. 300자 내로 설명해주세요. 출처는 포함하지 않습니다.'}
#     ]
#     for history in history_list[-1:-6:-1]:
#         for h, r in zip(history, ['user', 'assistant']):
#             gpt_messages.append({
#                 'role': r,
#                 'content': h
#             })
#     gpt_messages.append({
#         'role': 'user',
#         'content': '지금까지 대화를 요약해줘'
#     })
#     summary_history = openai.ChatCompletion.create(
#         model=model,
#         messages=gpt_messages,
#         temperature=0.15
#     )
#     return summary_history['choices'][0]['message']['content']

def GPTf(
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

    # 히스토리 요약 500토큰 이내로 ~ 500자 정도
    # summary_history = get_summary_history(history_list)

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