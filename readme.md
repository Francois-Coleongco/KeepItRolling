plan:

use openai whisper local in python to get the segments where there is speech.

based on the locations where there is speech, single out the contiguous sections, and ask an LLM to confirm coherence.

coherence check will be done by ollama local LLM.

after coherence check, you can label the video chunk with a short description of what it's about as well as the `tag`


dependencies

sudo apt-get install ffmpeg
curl -fsSL https://ollama.com/install.sh | sh
pip install git+https://github.com/snakers4/silero-models
