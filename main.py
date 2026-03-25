from contextlib import asynccontextmanager

from fastapi import Body, FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from bd import Base, add_request_data, engine, get_user_requests
from gemini_client import get_answer_from_gemini


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    print("Все таблицы созданы!")
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500",
                   "http://http://127.0.0.1:5500",
                   "http://localhost:5501",
                   "http://127.0.0.1:5501",
                   ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/requests")
def get_my_requests(request: Request):
    user_ip_adress = request.client.host
    print(f"Получен запрос от IP-адреса: {user_ip_adress}")
    user_requests = get_user_requests(ip_adress=user_ip_adress)
    return jsonable_encoder(user_requests)

@app.post("/requests")
def send_prompt(
    request: Request,
    prompt: str = Body(embedded=True)
    ):
    user_ip_adress = request.client.host
    answer = get_answer_from_gemini(prompt)
    add_request_data(
        ip_adress=user_ip_adress,
        prompt=prompt,
        response=answer,
        )
    return {"answer": answer}

