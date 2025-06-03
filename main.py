from fastapi import FastAPI
from database import engine, Base
import uvicorn
from src.routers import setup_routers

# Создание бд на основе моделей в models.py
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Добавляем все ручки в приложение
setup_routers(app)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)