import numpy as np
from segment import Segment
import ollama
from silero import silero_te

def repunctuate(dat: str):
    dat = dat.lower()
    model, _, _, _, apply_te = silero_te()
    punctuated_text = apply_te(dat, model)
    return punctuated_text


def ollama_passthrough(dat: str):
    dat = repunctuate(dat)
    print("dat was", dat)
    if dat == "":
        raise ValueError("passed in empty string to ollama_passthrough")

    resp = ollama.generate('llama3.2', f"""
    You are a coarse filter for human speech. Your only task is to flag text that is completely and utterly unintelligible.

    Return "false" **only** if the text is pure gibberish with no trace of coherent human language (e.g., "asdf jkl; qwerty", "the cat blue inherently"). This is for random word salad, not for bad or awkward writing.

    Return "true" for **everything else**. This includes:
    - Text with poor grammar, bad spelling, or weird punctuation.
    - Text with "um", "uh", or hesitations.
    - Text that is a single word or a fragment.
    - Technical jargon, even if used incorrectly.
    - Strange or illogical statements that a human might still say.
    - Repetitive or boring statements.
    - Be VERY lenient.

    If a reasonable human could utter the text in any context, return "true".
    Text: "{dat}"
    """)

    print(resp['response'])

    return "true" in resp['response'].lower()


def process_segments(segments: list[Segment]) -> list[Segment]:
    length = len(segments)
    # should change the return type to list perhaps if not doing the splitting logic in here

    ret: list[Segment]= []

    # get the contiguous (by threshold) segments and group them into a new list that is ret
    # use a sliding window

    threshold = np.float64(2) # should be something user defined in a config and/or part of flags

    i = 0

    if length == 1:
        if ollama_passthrough(segments[0].text):
            ret.append(Segment(segments[0].start, segments[0].end,
                              np.float64(10000.0), segments[0].text))
        return ret

    for j in range(1, length):
        curr_gap = segments[j].start - segments[j - 1].end

        if curr_gap > threshold:
            contiguous = "".join(s.text for s in segments[i:j])
            if ollama_passthrough(contiguous):
                ret.append(Segment(segments[i].start, segments[j - 1].end, np.float64(10000), contiguous))

            i = j

    contiguous_text = "".join(seg.text for seg in segments[i:length])

    if ollama_passthrough(contiguous_text):
        ret.append(Segment(segments[i].start, segments[length-1].end,
                      np.float64(10000.0), contiguous_text))


    return ret
