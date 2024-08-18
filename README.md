# 소개
### FastAPI 와 LangChain + RAG 를 사용한 대화형 AI 연습 프로젝트

<img width="993" alt="스크린샷 2024-08-18 오전 9 45 43" src="https://github.com/user-attachments/assets/083f0935-f8d6-403a-9ba3-4a167ed33f42">

### 사용 방법
```
RAG 에 활용할 문서를 아래 빨간색 박스로 표시한 부분을 통해 업로드 해주세요.
문서 용량에 따라 RAG 에서 사용하는 저장소에 저장되는 시간이 길어질 수 있습니다.
저장이 완료되면 완료 메세지가 표시됩니다.
```
![스크린샷 2024-08-18 오후 5 58 11](https://github.com/user-attachments/assets/d8e0bb7f-35ad-4e38-b942-0961e73eae53)

![스크린샷 2024-08-18 오후 6 00 25](https://github.com/user-attachments/assets/7ecdaeb6-7cc6-4d43-88aa-bc8a5c0c690f)

### 사용 예시 화면
- RAG

![화면 기록 2024-08-17 오후 6 37 22](https://github.com/user-attachments/assets/77ee5bd1-989c-4325-8894-248a5dc69b04)

<br/>

- Multi Modal

![2024-08-185 48 56-ezgif com-resize](https://github.com/user-attachments/assets/8cf1d7c3-1ce0-45fc-83bc-3e5cb29e269b)

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
- 선택한 이미지에 대한 질답

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
git clone https://github.com/SimJunSik/rag_agent_example.git

cd rag_agent_example
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

* 만약, 최초 서버 실행 후 파일 업로드가 실패한다면 **터미널 종료 후** 가상 환경 활성화 후에 서버를 **다시 실행** 해주세요.


### UI
```
http://127.0.0.1:8000/
```

<br/><br/>
