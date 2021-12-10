# coding=utf8
# import nltk
# nltk.download('punkt')
from flask import Flask, redirect, url_for, request, jsonify
from nltk import word_tokenize
import langid
from elt import translit

from model import get_translation

app = Flask(__name__)


def convert_text(text):
    if langid.classify(text)[0] == 'hi' or langid.classify(text)[0] == 'mr' \
            or langid.classify(text)[0] == 'ne' or langid.classify(text)[0] == 'zh':
        return text
    else:
        to_hindi = translit('hindi')
        text = to_hindi.convert([text])[0]
        return text


def to_devanagari(text):
    tokens = word_tokenize(text)
    # print(tokens)

    detect_lang_tokens = list(map(lambda x: langid.classify(x)[0], tokens))
    # print(detect_lang_tokens)

    result = list(map(convert_text, tokens))
    # print(result)

    devanagari_text = ' '.join(result)
    # print(devanagari_text)

    return devanagari_text


translation = {
    'input_text': '',
    'hindi_text': 'यहाँ दिए गए वाक्य का अनुवाद यह रहा!',
    'eng_text': 'Here is the English Translation of the given sentence!'
}


@app.route('/', methods=['GET'])
def home():
    response = jsonify(translation)
    return response


@app.route('/translate', methods=['GET'])
def translate():
    text = request.args['text']
    translation['input_text'] = text
    translation['hindi_text'] = to_devanagari(translation['input_text'])
    translation['eng_text'] = get_translation(translation['hindi_text'])
    response = jsonify(translation)
    return response


if __name__ == '__main__':
    app.run(debug=True)
