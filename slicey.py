import ffmpeg

def split_and_write_vid(vid_path: str, start: str, stop: str, tag: int, dir: str = '.'):
    s = vid_path.split('.')
    outfile = s[-2] + f"_EDIT_{tag}" + s[-1]
    ffmpeg.input(vid_path, ss=start).output(outfile, stop - start, )
