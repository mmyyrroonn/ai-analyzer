from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from dotenv import load_dotenv
import time

# get data directory (using getcwd() is needed to support running example in generated IPython notebook)
d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir,os.path.pardir,'.env'))
load_dotenv(dotenv_path=dotenv_path)

class AIPicGenerator:
    def __init__(self):
        self.mask_coloring = np.array(Image.open(path.join(d, "alice_color.png")))
        self.image_colors = ImageColorGenerator(self.mask_coloring)
        self.env_path = os.getenv('AI_TAG_PATH')
        self.tags_count = 10

    def generate_word_cloud_pic_with_mask(self, words, profile):        
        wc = WordCloud(background_color="white", max_words=2000, mask=self.mask_coloring, max_font_size=40, random_state=42)
        # generate word cloud
        keywords = []
        for data in words.values():
            keywords.extend(data)
        text = ' '.join(keywords)
        wc.generate(text)
        wc.recolor(color_func=self.image_colors)
        image_name = str(profile) + "-" + str(int(time.time())) + ".png"
        img_path = os.path.abspath(os.path.join(self.env_path, image_name))
        wc.to_file(img_path)
        return img_path

    def generate_word_cloud_pic(self, words, profile, nftid=""):        
        wc = WordCloud(width=1600, height=400, max_words=200, min_font_size=10, max_font_size=150, random_state=42, mode="RGBA", background_color=None, colormap="RdGy_r")
        # generate word cloud
        keywords = []
        for data in words.values():
            keywords.extend(data)
        text = ' '.join(keywords)
        wc.generate(text)
        image_name = str(profile) + "-" + str(nftid) + '-' + str(int(time.time())) + ".png"
        img_path = os.path.abspath(os.path.join(self.env_path, image_name))
        wc.to_file(img_path)
        words_tags = [item[0] for item in list(wc.words_.items())[:self.tags_count]]
        return image_name, words_tags