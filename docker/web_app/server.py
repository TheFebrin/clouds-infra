#!/usr/local/bin/python
import os
from flask import Flask
from gensim.utils import tokenize

app = Flask(__name__)

@app.route('/')
def main():
    var = os.environ['DEV']
    return f'<p>DEV: {var} Give me a sentence after /</p>'

@app.route('/<sentence>')
def tokenize_endpoint(sentence):
    var = os.environ['DEV']
    if var == 'prod':
        ans = 'Your result:' + ''.join(list(tokenize(sentence, lowercase=True, deacc=True)))
    elif var == 'staging':
        ans = 'WARNING STAGING VERSION\n' + 'Your result:' + ''.join(list(tokenize(sentence, lowercase=True, deacc=True)))
    else:
        ans = f'WRONG DEV variable: {var}'
    return ans

if __name__ == "__main__":
    app.run(host='0.0.0.0')