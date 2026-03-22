from input_parameters import quote, author, outputName
from util import select_audio

input_dict = {
  "quote": quote,
  "author": author,
  "outputName": outputName,
  "font": "fonts/font.ttf",
  "audio": "audios/" + select_audio(quote),
  "imagesPath": "./images/images2",
  "random": True,
  "bg_img_opacity": 0.2,
  "bg_img_duration": 0.3,
}