import numpy as np
from segment import Segment
import ollama
import torch
import torch

model, example_texts, languages, punct, apply_te = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                                                  model='silero_te', languages="en")

def repunctuate(dat: str):
    print("this is the repunctuated?", apply_te(dat, lan='en'))


def ollama_passthrough(dat: str):
    dat = repunctuate(dat)
    print("dat was", dat)
    if dat == "":
        raise ValueError("passed in empty string to ollama_passthrough")

    resp = ollama.generate('llama3.2', f"""
    You are analyzing a transcript segment from a video.

    Decide if the text is coherent and conveys a meaningful idea.
    - Do NOT penalize run-on sentences.
    - Do NOT mark it incoherent just because of spelling errors or unknown words.
    - Only return "true" if the text overall makes sense as human speech or explanation.
    - Return "false" only if the text is pure nonsense or word salad.

    Reply with ONLY "true" or "false".

    Text: "{dat}"
    """)

    print(resp['response'])

    return "true" in resp['response']


def process_segments(segments: list[Segment]):
    length = len(segments)
    # should change the return type to list perhaps if not doing the splitting logic in here

    ret = []

    # get the contiguous (by threshold) segments and group them into a new list that is ret
    # use a sliding window

    threshold = np.float64(2) # should be something user defined in a config and/or part of flags

    i = 1
    j = 1

    new_start = segments[0].start
    new_end = segments[0].end

    contiguous = segments[0].text
    print("initialized contiguous was", contiguous)
    ended_in_mid = 0

    while j < length:
        print(f"looping, end of last: {segments[j - 1].end} start of next: {segments[j].start} with text: {contiguous}")
        if not (segments[j].start - segments[j - 1].end <= threshold):
            print("made it in here?")
            new_end = segments[j - 1].end

            contiguous = "".join(s.text for s in segments[i:j + 1])

            i = j

            if ollama_passthrough(contiguous):
                print(f"appending segment containing: \"{contiguous}\" between {new_start} and {new_end}.")
                ret.append(Segment(new_start, new_end, np.float64(10000.0), contiguous))

            new_start = segments[j].start

            contiguous = ""
        else:
            ended_in_mid = 1

        j += 1

    if ended_in_mid:
        contiguous = contiguous + "".join(s.text for s in segments[i:j + 1])
        if ollama_passthrough(contiguous): # not empty
            print(f"attempting to add last chunk, {contiguous}")
            ret.append(Segment(new_start, new_end, np.float64(10000.0), contiguous))


    return ret
