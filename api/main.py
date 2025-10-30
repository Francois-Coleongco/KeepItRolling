import time
from fastapi import FastAPI, Form, UploadFile, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

import secrets
from hashlib import sha256
import os

from fastapi.responses import FileResponse
from split_entry import agnostic_to_platform_splitter
import common

os.makedirs(common.UPLOAD_DIR, exist_ok=True)
os.makedirs(common.OUTPUT_DIR, exist_ok=True)

allowed_extensions = (".mp4", ".mkv")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/split-vid")
async def split_vid(request: Request, file: UploadFile, padding: int = Form(...)):

    client_ip = request.client
    if client_ip == None:
        return {"message": "how do you not have an ip??"}

    if file.filename == None:
        return {"message": "could not upload file with no name"}

    if not file.filename.endswith(allowed_extensions):
        return {"message": "unsupported file type"}

    random_secret = str(secrets.randbits(64))

    hash_data = client_ip.host + str(time.time()) + file.filename + random_secret

    hash = sha256(hash_data.encode("utf-8")).hexdigest()

    new_file_name = str(hash) + "." + file.filename.rsplit(".", 1)[-1]

    contents = await file.read()

    with open(os.path.join(common.UPLOAD_DIR, new_file_name), "wb") as f:
        f.write(contents)

    return {"message": agnostic_to_platform_splitter(common.UPLOAD_DIR + new_file_name, padding)}


@app.get("/get-vid")
async def get_vid(file_name: str):
    if file_name == "":
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Must Provide non-empty file name"
        )

    try:
        file_path = os.path.join(common.OUTPUT_DIR, file_name)
        return FileResponse(
            path=file_path,
            filename=file_name,
            media_type="application/octet-stream"
        )

    except Exception as e:
        print(f"error getting file on get_vid endpoint {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not retrive file from system")

