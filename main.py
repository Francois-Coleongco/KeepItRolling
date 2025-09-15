import pre
import audio
import argparse
import context

def main():

    parser = argparse.ArgumentParser("")
    parser.add_argument("-v", "--video", type=str, help="please enter a valid video path e.g. ./vid.mp4")
    parser.add_argument("-p", "--padding", type=int, help="enter padding in seconds between clips")
    args = parser.parse_args()

    audio_path=f"{args.video}_tmp_.wav"

    pre.extract_audio_from_vid(args.video, audio_path)
    segments = audio.transcribe_audio(audio_path, args.padding)

    if segments == None:
        raise ValueError("no audio segments found in video!")

    print(context.process_segments(segments))

if __name__ == "__main__":
    main()
