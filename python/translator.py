# translator.py
from googletrans import Translator

def translate_news(news_contents, src='auto', dest='en'):
    translator = Translator()
    return [translator.translate(content, src=src, dest=dest).text for content in news_contents]
