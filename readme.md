# KeepItRolling

<img width="1475" height="1105" alt="system_design_diagram" src="https://github.com/user-attachments/assets/7aa595d3-3948-4607-917b-909416c272e8" />

Demo:

https://github.com/user-attachments/assets/084c65dd-2efe-4466-ae74-783b52fdbc6e




The aim is to keep the camera rolling without having to manage so many recordings and sift through relevant ones manually.

KeepItRolling is a project that processes video and audio files, detects speech segments, checks coherence, and generates summaries and tags for those segments using local ML models.

The **core model logic is implemented and working**, while the **FastAPI service layer is still a work in progress**.

---

## Features

- Splits video/audio into segments where speech is detected.  
- Checks coherence of speech segments using a local LLM (Ollama).  
- Tags / labels each segment with short descriptions.  
- Uses OpenAI Whisper for speech extraction, Silero-models for repunctuation before feeding into coherence check.
- Exposed as an API with **FastAPI** and **React** interface.

- Planned - Timed deletions of videos in the ./api/OUTPUTS/ directory. (get the file creation date, and compare to current, and if after certain threshold, delete), perhaps do this as a cron job?


## FastAPI

### POST /split-vid
Process a video file.

**Expected request:**
- Multipart/form-data with video file upload.
- Padding - (integer value for how many seconds you want between output clips).

**Expected response:**

- a list of file names of split videos


### GET /get-vid
Retrieve a video file.

**Expected request:**
- Query parameter containing the video name one wishes to download.

**Expected response:**

- the video file as a downloadable blob


---

## Usage

In terminal 1:
```
python3 -m venv venv
source ./venv/bin/activate
pip3 install -r requirements.txt
cd api/
fastapi dev main.py
```

In terminal 2:
```
cd frontend/
npm run dev
```

Now you can visit `http://127.0.0.1:5173/`


## Deployment

Coming soon :)
