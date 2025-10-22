# KeepItRolling

<img width="1475" height="1105" alt="system_design_diagram" src="https://github.com/user-attachments/assets/7aa595d3-3948-4607-917b-909416c272e8" />

The aim is to keep the camera rolling without having to manage so many recordings and sift through relevant ones manually.

KeepItRolling is a project that processes video and audio files, detects speech segments, checks coherence, and generates summaries and tags for those segments using local ML models.

The **core model logic is implemented and working**, while the **FastAPI service layer is still a work in progress**.

---

## Features

- Splits video/audio into segments where speech is detected.  
- Checks coherence of speech segments using a local LLM (Ollama).  
- Tags / labels each segment with short descriptions.  
- Uses OpenAI Whisper for speech extraction, Silero-models for repunctuation before feeding into coherence check.
- Designed to be exposed as an API with **FastAPI** (in progress).

---

## Current

- Core model logic (speech detection, coherence checks, tagging)

- FastAPI service layer (endpoints, request/response handling)  

---

## FastAPI

### POST /split-vid
Process a video or audio file.

**Expected request:**
- Multipart/form-data with video file upload.
- Optional query parameters for configuration.

**Expected response:**
- JSON containing:
  - Segment timestamps
  - Transcriptions  

  **Planned:**
  - Coherence check results
  - Tags/labels

---

## Usage

Right now, you can use the API through SwaggerUI, React frontend is in progress.

```

python3 -m venv venv
source ./venv/bin/activate
pip3 install -r requirements.txt
cd api/

fastapi dev main.py

```

You can now upload at 127.0.0.1:800/docs
