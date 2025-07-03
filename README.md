Image Moderation API
FastAPI + Sightengine

Микросервис для автоматической модерации изображений с использованием Sightengine API. Определяет NSFW-контент и возвращает результат в стандартизированном формате.

# 1.  Запуск
   
1) Локальный запуск (без Docker)
Установка зависимостей

pip install -r requirements.txt

Запуск сервера

uvicorn main:app --reload

2) Через докер
Сборка образа

docker build -t image-moderation .

Запуск контейнера

docker run -p 8000:8000 image-moderation

Откройте в браузере http://localhost:8000/docs

или отправьте тестовый запрос curl -X POST -F "file=@your_image.jpg" http://localhost:8000/moderate

# 2. Примеры запросов:
1) Успешная модерация
        {
    "status": "OK"
  }
2) Обнаружен nsfw контент
      {
  "status": "REJECTED",
  "reason": "NSFW content"
}
3) Ошибка
   {
  "status": "REJECTED",
  "reason": "NSFW content"
}
# 3. Порог срабатывания : if nsfw_score > 0.7
