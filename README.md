# 소개
### FastAPI 와 LangChain + RAG 를 사용한 대화형 AI 연습 프로젝트

<img width="993" alt="스크린샷 2024-08-18 오전 9 45 43" src="https://github.com/user-attachments/assets/b9ec7c7e-4862-480c-bdba-3d526c1eb48d">

</br><br/>

# 기술 스택
- FastAPI
- LangChain
- ChatOpenAI
- OpenAIEmbeddings
- Chroma
- sqlite

<br/><br/>

# 구현 내용
- Embedding 된 문서들 내에서의 질답
- 대화를 이어나갈 수 있는 메모리
- Streaming 을 통한 챗봇 UI
- File upload 를 통한 문서 추가

<br/><br/>

# 환경 구축
### 디렉토리 생성
```
mkdir <folder_name>
cd <folder_name>
```

### 가상환경 생성 및 활성화
```
python3.9 -m venv venv

source venv/bin/activate
```

### git clone
```
git clone https://github.com/SimJunSik/rag_agent_ex.git

cd rag_agent_ex
```

### 라이브러리 설치
```
pip install -r requirements.txt
```

### OpenAI API Key 등록
```
프로젝트 루트 디렉토리에 `.env` 파일 생성, 아래와 같이 OpenAI API Key 추가

OPENAI_API_KEY=your_openai_api_key_here
```

### 서버 실행
```
uvicorn main:app --reload
```

### UI
```
http://127.0.0.1:8000/
```

<br/><br/>

# 사용 예시 화면
![화면 기록 2024-08-17 오후 6 37 22](https://github.com/user-attachments/assets/d36e6585-7d24-4578-92d8-1341283befba)
