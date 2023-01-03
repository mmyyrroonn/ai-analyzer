from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

# get data directory (using getcwd() is needed to support running example in generated IPython notebook)
d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
class AITagGenerator:
    def __init__(self):
        self.mask_coloring = np.array(Image.open(path.join(d, "nosocial.png")))
        self.image_colors = ImageColorGenerator(self.mask_coloring)

    def generate_word_cloud_pic(self, text):        
        wc = WordCloud(background_color="white", max_words=2000, mask=self.mask_coloring, max_font_size=40, random_state=42)
        # generate word cloud
        wc.generate(text)
        wc.recolor(color_func=self.image_colors)
        wc.to_file("generated_ai_tag.png")