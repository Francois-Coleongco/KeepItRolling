from typing import Optional
import numpy as np
import whisper
from segment import Segment

def transcribe_audio(audio_path: str, padding: int) -> Optional[list[Segment]]:
    try:
        model = whisper.load_model("medium.en") # change this to a multilingual one for cross language support in the future, for now just english for development
        result = model.transcribe(
            audio_path,
            word_timestamps=True,
            verbose=True,
            fp16=False,
            temperature=0.0,
            best_of=5,
            condition_on_previous_text=False
        )

        Segment.padding = padding

        segments: list[Segment] = []

        key = 0

        for segment in result['segments']:
            s: Segment = Segment(segment['start'], segment['end'], np.float64(10000.0), segment['text'])
            segments.append(s)
            key += 1



        print("Transcription: ", result)
        return segments

    except Exception as e:
        print("error transcribing: ", e)
        return None


