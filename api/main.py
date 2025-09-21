from fastapi import FastAPI, UploadFile, File, Request
import secrets
from hashlib import sha256


allowed_extensions = tuple(i for i in [".mp4", ".mkv"])

app = FastAPI()

@app.post("/upload")
async def root(file: UploadFile, request: Request):

    client_ip = request.client
    if client_ip == None:
        return {"message", "how do you not have an ip??"}

    if file.filename == None:
        return {"message", "could not upload file with no name"}

    file.filename.endswith(allowed_extensions)
    username = "" # compare request data to user database to fill this field in the future

    random_secret = str(secrets.randbits(64))

    hash_data = client_ip.host + username + random_secret + file.filename # someone could have same ip aka same network and sending same file name and then they get a collision, no bueno

    # if the request is authenticated, aka requester has an account, we will use their username + a random secret along with data to hash

    hash = sha256(hash_data.encode("utf-8"))

    new_file_name = str(hash) + "." + file.filename.rsplit(".", 1)[-1]

    with open(new_file_name, "wb") as f:
        contents = await file.read()
        await file.write(contents)

    return {"message": "successfully uploaded"}


