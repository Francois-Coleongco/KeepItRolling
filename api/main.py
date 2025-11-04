from datetime import datetime
from fastapi import Depends, FastAPI, Form, UploadFile, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import secrets
from hashlib import sha256
import os

from fastapi.responses import FileResponse
from split_entry import agnostic_to_platform_splitter

from common import UPLOAD_DIR, OUTPUT_DIR, UserInDB
from auth import get_current_user, authenticate_user, create_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

allowed_extensions = (".mp4", ".mkv")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/split-vid")
async def split_vid(request: Request, file: UploadFile, padding: int = Form(...), current_user: UserInDB = Depends(get_current_user)):

    client_ip = request.client
    if client_ip == None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="how do you not have an ip??")

    if file.filename == None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no file name provided")

    if not file.filename.endswith(allowed_extensions):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid file extension")

    random_secret = str(secrets.randbits(64))

    hash_data = client_ip.host + str(datetime.now()) + file.filename + random_secret

    hash = sha256(hash_data.encode("utf-8")).hexdigest()

    new_file_name = str(hash) + "." + file.filename.rsplit(".", 1)[-1]

    contents = await file.read()

    with open(os.path.join(UPLOAD_DIR, new_file_name), "wb") as f:
        f.write(contents)

    return {"message": agnostic_to_platform_splitter(UPLOAD_DIR + new_file_name, padding)}


@app.get("/get-vid")
async def get_vid(file_name: str):
    if file_name == "":
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Must Provide non-empty file name"
        )

    try:
        file_path = os.path.join(OUTPUT_DIR, file_name)
        return FileResponse(
            path=file_path,
            filename=file_name,
            media_type="application/octet-stream"
        )

    except Exception as e:
        print(f"error getting file on get_vid endpoint {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not retrive file from system")


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token(user.username)
    return {"access_token": token, "token_type": "bearer"}
