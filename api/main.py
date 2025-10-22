import time
from fastapi import FastAPI, UploadFile, Request
import secrets
from hashlib import sha256
import os
from split_entry import agnostic_to_platform_splitter

UPLOAD_DIR = "UPLOADS/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

allowed_extensions = (".mp4", ".mkv")

app = FastAPI()

@app.post("/split-vid")
async def split_vid(file: UploadFile, padding: int, request: Request):

    client_ip = request.client
    if client_ip == None:
        return {"message", "how do you not have an ip??"}

    if file.filename == None:
        return {"message", "could not upload file with no name"}

    if not file.filename.endswith(allowed_extensions):
        return {"message": "unsupported file type"}

    random_secret = str(secrets.randbits(64))

    hash_data = client_ip.host + str(time.time()) + file.filename + random_secret

    hash = sha256(hash_data.encode("utf-8")).hexdigest()

    new_file_name = str(hash) + "." + file.filename.rsplit(".", 1)[-1]

    contents = await file.read()

    with open(os.path.join(UPLOAD_DIR, new_file_name), "wb") as f:
        f.write(contents)

    return {"message": agnostic_to_platform_splitter(UPLOAD_DIR + new_file_name, padding)}


