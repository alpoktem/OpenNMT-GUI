#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify, request
from flask_wtf import FlaskForm
from flask_pagedown import PageDown
from flask_pagedown.fields import PageDownField
from wtforms.fields import SubmitField
import requests
import json
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
pagedown = PageDown(app)

url = "http://127.0.0.1:5000/translate"


class PageDownFormExample(FlaskForm):
    pagedown = PageDownField('Type the text you want to translate and click "Translate".')
    submit = SubmitField('Translate')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = PageDownFormExample()
    text = None
    language = "fr-sw" #Default
    if form.validate_on_submit():
        source = form.pagedown.data.lower()
        source = re.sub(r"([?.!,:;¿])", r" \1 ", source)
        source = re.sub(r'[" "]+', " ", source)
        language = str(request.form.get('lang'))

        src_language = language.split("-")[0]
        tgt_language = language.split("-")[1]

        headers = {"Content-Type": "application/json"}
        data = {"src": src_language, "tgt": tgt_language, "text": source}
        response = requests.post(url, json=data, headers=headers)
        translation_response = response.text
        print(translation_response)

        jsn = json.loads(translation_response)
        translated_text = jsn['translation']
    else:
        form.pagedown.data = ('This is a very simple test.')
    return render_template('index.html', form=form, language=language, text=translated_text)


if __name__ == '__main__':
    app.run(debug=True, port=6000)