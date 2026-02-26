from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fastapi import Request
import shutil
import os
from deepface import DeepFace

app = FastAPI()
templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def compare_faces(img1_path, img2_path):
    result = DeepFace.verify(
        img1_path,
        img2_path,
        model_name="Facenet512",
        detector_backend="retinaface"
    )

    distance = result["distance"]
    similarity = (1 - distance) * 100

    return {
        "verified": result["verified"],
        "distance": round(distance, 4),
        "similarity": round(similarity, 2)
    }

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("favicon.ico")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/compare")
async def compare(file1: UploadFile = File(...), file2: UploadFile = File(...)):

    img1_path = os.path.join(UPLOAD_FOLDER, file1.filename)
    img2_path = os.path.join(UPLOAD_FOLDER, file2.filename)

    with open(img1_path, "wb") as buffer:
        shutil.copyfileobj(file1.file, buffer)

    with open(img2_path, "wb") as buffer:
        shutil.copyfileobj(file2.file, buffer)

    result = compare_faces(img1_path, img2_path)

    return JSONResponse(content=result)