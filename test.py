from silero import silero_te

def repunctuate(dat: str):
    model, examples, langs, supported_punct, apply_te = silero_te()
    
    # Use the apply_te function on your text
    # It needs the model, the text, and the language code
    punctuated_text = apply_te(dat, model)
    return punctuated_text


punctuated = repunctuate("this is not punctuated i need grapes")
print(punctuated)
