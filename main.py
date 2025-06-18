from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import requests
import uuid

app = FastAPI()

AZURE_ENDPOINT = "https://face-api1111.cognitiveservices.azure.com/"
AZURE_KEY = "EqAu6yLWtQJy1YUC6XSoynu5nslLxkn2eIjaGk35LLH2R51IRPApJQQJ99BFACYeBjFXJ3w3AAAKACOGUTtg"

@app.post("/analyze/")
async def analyze_face(file: UploadFile = File(...)):
    try:
        image_data = await file.read()
        headers = {
            "Ocp-Apim-Subscription-Key": AZURE_KEY,
            "Content-Type": "application/octet-stream"
        }
        params = {
            "returnFaceAttributes": "age,gender,emotion,glasses",
        }

        response = requests.post(
            AZURE_ENDPOINT + "face/v1.0/detect",
            params=params,
            headers=headers,
            data=image_data
        )

        if response.status_code != 200:
            return JSONResponse(status_code=response.status_code, content=response.json())

        faces = response.json()
        return {"faces": faces}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
