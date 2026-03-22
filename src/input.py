from input_parameters import quote, author, outputName, imgGenre, random, audio, manual_audio
from util import select_audio

input_dict = {
  "quote": quote,
  "author": author,
  "outputName": outputName,
  "font": "fonts/font.ttf",
  "audio": audio if manual_audio else "audios/" + select_audio(quote),
  "imagesPath": "./images/images" + str(imgGenre),
  "random": random,
  "bg_img_opacity": 0.2,
  "bg_img_duration": 0.3,
}