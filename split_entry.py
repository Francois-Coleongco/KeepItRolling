from re import split
import pre
import audio
import argparse
import context
import slicey

def agnostic_to_platform_splitter(video: str, padding: int):

        if video == "":
            raise Exception("video name invalid")

        audio_path=f"{video}_tmp_.wav"

        pre.extract_audio_from_vid(video, audio_path)
        segments = audio.transcribe_audio(audio_path, padding)

        if segments == None:
            raise ValueError("no audio segments found in video!")

        makes_sense = context.process_segments(segments)

        print(f"this is makes sense: {makes_sense}")

        ret: list[str] = []

        tag = 0
        for seg in makes_sense:
            print(seg.start, seg.end)
            start = str(seg.start)
            end = str(seg.end)
            split_file = slicey.split_and_write_vid(video, start, end, tag)
            print("appending split_file: ", split_file)
            ret.append(split_file)
            tag += 1

        return ret



def split_entry():

    parser = argparse.ArgumentParser("")
    parser.add_argument("-v", "--video", type=str, help="please enter a valid video path e.g. ./vid.mp4")
    parser.add_argument("-p", "--padding", type=int, default=1, help="enter padding in seconds between clips")

    args = parser.parse_args()

    try:
        agnostic_to_platform_splitter(args.video, args.padding)

    except Exception as e:
        print("exception parsing args was:", e, "\nplease enter command in the form `python3 ./main.py --video media.mp4 --padding 1`")



if __name__ == "__main__":
    split_entry()
