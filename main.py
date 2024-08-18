import base64
from fastapi import (
    FastAPI,
    Form,
    HTTPException,
    File,
    UploadFile,
    Body,
    Request,
    Response,
)
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from services.db import DBService
from services.generate_answer import GenerateAnswerService
from services.vector_db import VectorDBService
from dotenv import load_dotenv
from uuid import uuid4

import langchain

langchain.debug = False

load_dotenv()


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

vector_db_service = VectorDBService()
vector_db_service.init_vector_db()

generate_answer_service = GenerateAnswerService()
DBService.init_db()


@app.middleware("http")
async def cookie_middleware(request: Request, call_next):
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid4())

    response: Response = await call_next(request)
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    return response


@app.post("/ask")
async def ask_question(query: str = Body(..., embed=True)) -> dict:
    try:
        result = generate_answer_service.generate_answer(query=query)
        return {"result": result}
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ask_stream")
async def ask_question_stream(
    request: Request, query: str = Form(...), file: UploadFile = File(None)
) -> StreamingResponse:
    session_id = request.cookies.get("session_id")
    encoded_content = None
    if file:
        content = await file.read()
        encoded_content = base64.b64encode(content).decode("utf-8")
    gen = generate_answer_service.generate_answer_with_stream(query, session_id, encoded_content)
    return StreamingResponse(gen, media_type="text/event-stream")


@app.get("/")
async def get() -> HTMLResponse:
    with open("static/index.html") as f:
        return HTMLResponse(content=f.read())


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)) -> dict:
    file_location = f"documents/{file.filename}"

    try:
        with open(file_location, "wb") as f:
            f.write(file.file.read())

        vector_db_service.embed_document(file.filename)
        return {"info": f"file '{file.filename}' saved at '{file_location}'"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {e}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
