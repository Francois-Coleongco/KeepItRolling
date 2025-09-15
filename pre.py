import ffmpeg

TEMP_MARKING: str = "tmp-"
#     audio_path = video_file.split(".")[0] + ".wav"


def extract_audio_from_vid(video_file: str, audio_path: str):
    try:
        stream = ffmpeg.input(video_file)
        stream = ffmpeg.output(stream, audio_path, format='wav', acodec='pcm_s16le', ar=16000)
        ffmpeg.run(stream)
        print(f"Audio extracted to {audio_path}")
    except ffmpeg.Error as e:
        print(f"Error extracting audio: {e.stderr.decode()}")
        raise
