from segment import Segment
import ollama

def ollama_passthrough(dat: str):
    print("dat was", dat)

    resp = ollama.generate('llama3.2', "Decide if this text is coherent and meaningful (not gibberish). Reply ONLY with \"true\" or \"false\"." + dat)

    return "true" in resp['response']


def process_segments(segments: list[Segment]):
    # should change the return type to list perhaps if not doing the splitting logic in here

    ret = []

    for segment in segments:
        print("this was segment.text", segment.text)
        if ollama_passthrough(segment.text):
            ret.append(segment)

    return ret
