from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import requests


app = FastAPI()


SIGHTENGINE_API_USER = "686861647"
SIGHTENGINE_API_SECRET = "NNPzfc7NwaknnMZxV7oQGVTSGgg5Bz5b"
SIGHTENGINE_API_URL = "https://api.sightengine.com/1.0/check.json"


@app.post("/moderate")
async def moderate_image(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(status_code=400, detail="Файл должен быть .png или .jpg")

    try:
        contents = await file.read()

        files = {'media': contents}
        params = {
            'models': 'nudity-2.0',
            'api_user': SIGHTENGINE_API_USER,
            'api_secret': SIGHTENGINE_API_SECRET
        }

        response = requests.post(SIGHTENGINE_API_URL, files=files, data=params)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"ошибка при запросе к Sightengine API: {response.text}"
            )

        result = response.json()
        nsfw_score = result.get('nudity', {}).get('sexual_activity', 0)

        if nsfw_score > 0.7:
            return JSONResponse(content={"status": "REJECTED", "reason": "NSFW content"})
        else:
            return JSONResponse(content={"status": "OK"})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обработке изображения: {str(e)}")


# curl -X POST -F "file=@test.jpg" http://127.0.0.1:8000/moderate