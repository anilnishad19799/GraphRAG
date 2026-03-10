import os
import subprocess
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
import os
from dotenv import load_dotenv
from dotenv import find_dotenv

load_dotenv(override=True)
app = FastAPI()

ROOT_DIR = "."
INPUT_DIR = os.path.join(ROOT_DIR, "input")

os.makedirs(INPUT_DIR, exist_ok=True)

# Serve UI
@app.get("/")
async def home():
    return FileResponse("index.html")


# Upload File
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(INPUT_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {"message": "File uploaded successfully"}

# Run Index
@app.post("/index/")
async def run_index():

    result = subprocess.run(
        ["graphrag", "index", "--root", ROOT_DIR],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("result.stderr",result)
        return JSONResponse(
            {"error": result.stderr},
            status_code=500
        )

    return {"message": "Index created successfully"}


# Query
@app.post("/query/")
async def run_query(question: str = Form(...), mode: str = Form(...)):

    result = subprocess.run(
        [
            "graphrag",
            "query",
            question,
            "--method",
            mode
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return JSONResponse(
            {"error": result.stderr},
            status_code=500
        )

    return {"answer": result.stdout}
