import numpy as np

class Segment:
    video_len = 0
    padding = 0 # changed in main if padding arg is passed by user
    text = ""

    def __init__(self, start: np.float64,  end: np.float64, vid_end: np.float64, text: str):
        start = np.round(start).astype(int)
        self.video_len = vid_end;
        self.text = text
        self.start = start if start - self.padding >= 0 else 0
        self.end = np.round(end).astype(int) + self.padding # might needa check upper bound
