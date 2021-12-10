# coding=utf8
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


def get_translation(devanagari_text):
    tokenizer = AutoTokenizer.from_pretrained("salesken/translation-hi-en")
    model = AutoModelForSeq2SeqLM.from_pretrained("salesken/translation-hi-en")

    hin_snippet = devanagari_text
    inputs = tokenizer.encode(
        hin_snippet, return_tensors="pt", padding=True, max_length=512, truncation=True)

    outputs = model.generate(
        inputs, max_length=128, num_beams=None, early_stopping=True)

    translated = tokenizer.decode(outputs[0]).replace('<pad>', "").strip().lower()

    return translated


# print('English Translation -> ', get_translation('क्या फालतू लोग है यह लोग'))
