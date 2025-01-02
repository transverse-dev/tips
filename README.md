# 개요

**제품 설명**

- **1:1 화상 통신 환경(webRTC)에서 실시간 집중도 파악 및 회의 내용 요약 기능이 통합되어 나타나는 시스템**

**기술 스택**

- 실시간 집중도 파악
    - GazeTracking : eye tracker
    - 68 face landmarks : head angle tracker
- STT
    - OpenAI Whisper Model : Speach to Text translation
    - GPT 3.5-turbo Model : Script Summarization
- WEB 환경
    - Streamlit
    - Streamlit-webrtc

# 실시간 집중도 파악 기능

**Eye Tracker**

- GazeTracking 오픈소스를 활용하여 눈동자의 위치를 파악하고 양 옆의 흰자 비율을 파악합니다. 이를 통해 눈동자가 정면/왼쪽/오른쪽 중 어느 곳을 바라보는지 추적합니다. 일정 비율 이상 눈동자가 벗어나면 경고 표시를 띄웁니다.

**Head Angle Tracker**

- 68 face landmarks 중 코 끝부분과 얼굴의 왼쪽, 오른쪽 점을 각각 이어 가로 선을 그립니다. 가로 선의 길이 차이가 일정 비율을 넘어가면 고개를 돌리고 주의 집중이 흩어진 것으로 판단합니다. 일정 비율 이상 고개가 돌아가면 경고 표시를 띄웁니다.

# 실시간 회의 내용 요약 기능

**Audio Real-time Recording**

- Realtime Streaming으로 회의 내용을 녹음합니다. 40초에 한 번씩 회의 내용 요약 함수를 호출합니다. Threading으로 녹음과 회의 내용 요약은 병렬로 진행됩니다.

**STT (Speach to Text)**

- OpenAI Whisper Model로 40초 분량의 음성 파일을 텍스트로 변환합니다.

**Summarization**

- 텍스트로 변환한 회의 내용을 GPT 모델로 요약합니다. 이전 회의 내용도 참고하여 요약합니다.

**Output Recording**

- 요약 파일을 텍스트 파일에 기록합니다.

# 시연

https://youtu.be/-Euf2UuHqmw

# 후속 개선 사항

- Whisper Model 성능 향상 방안 : Whisper-Jax 모델 연구 || OpenAI Whisper API 사용
- Streamlit-webrtc 네트워크 연결
- STT 모델 API로 변경 (유료)

# 마무리

개발 기간이 늘어져서 죄송합니다. 두 달 동안 뜻 깊은 경험이었습니다. 다음에 다른 프로젝트에 불러주시면 지금보다 훨씬 성장한 모습으로 돌아오겠습니다. 감사합니다.
