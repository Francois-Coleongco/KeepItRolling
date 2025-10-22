import ffmpeg

def split_and_write_vid(vid_path: str, start: str, stop: str, tag: int) -> str:
    s = vid_path.rsplit('.', 1) # split once near the end

    outfile = "OUTPUTS/" + s[-2].replace("UPLOADS/", "", 1) + f"_EDIT_{tag}." + s[-1]

    print(f"attempting to split into outfile: {outfile}")

    try:
        ffmpeg.input(vid_path, ss=start, to=stop).output(outfile).run()
        return outfile
    except Exception as e:
        print(f"what {e}")
        return ""

# split_and_write_vid("tcp_short.mp4", "00:00:00", "00:00:50", 0)
