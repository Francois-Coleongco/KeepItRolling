# KeepItRolling

The aim is to keep the camera rolling without having to manage so many recordings and sift through relevant ones manually.

KeepItRolling is a project that processes video and audio files, detects speech segments, checks coherence, and generates summaries and tags for those segments using local ML models.

The **core model logic is implemented and working**, while the **FastAPI service layer is still a work in progress**.

---

## Table of Contents

- [Features](#features)  
- [Current Status](#current-status)  
- [Planned API](#planned-api)  
- [Usage](#usage)  
- [Project Structure](#project-structure)  
- [Testing](#testing)  
- [Contributing](#contributing)  
- [License](#license)  
- [Acknowledgements](#acknowledgements)

---

## Features

- Splits video/audio into segments where speech is detected.  
- Checks coherence of speech segments using a local LLM (Ollama).  
- Tags / labels each segment with short descriptions.  
- Uses OpenAI Whisper (locally) and Silero-models for speech detection.  
- Designed to be exposed as an API with **FastAPI** (in progress).  

---

## Current Status

✅ Core model logic (speech detection, coherence checks, tagging)  
🚧 FastAPI service layer (endpoints, request/response handling)  

You can already run the logic modules directly, but the REST API is still being integrated.

---

## Planned API

### `POST /upload (planned)
Process a video or audio file.

**Expected request:**
- Multipart/form-data with file upload (audio/video).
- Optional query parameters for configuration.

**Expected response:**
- JSON containing:
  - Segment timestamps  
  - Transcriptions  
  - Coherence check results  
  - Tags/labels  

---

## Usage

Right now, you can run the main.py file in the vietual environment directly to process audio/video.

But in the future, will be accessible via this link --> future me, pls put something here-