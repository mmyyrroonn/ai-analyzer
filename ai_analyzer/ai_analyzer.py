"""Main module."""

from flask import Flask
from .analyzer import main as AIAnalyzer

app = Flask(__name__)

@app.route('/')
def hello():
    ai_analyzer = AIAnalyzer("qiufan_glamour@outlook.com", "qf19931115")
    content = "Orb, not even close. PFP same everywhere including iCloud and Google accounts, mainly so I can quickly identify which account I’m on rather than promoting anything."
    results = ai_analyzer.query_key_words_for_post(content)
    return "Hello, NoSocial! {}".format(results)
