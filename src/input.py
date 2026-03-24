# For convienience, edit the `input_parameters.py` file to tune your parameters.
# Only change this dict directly if you know what you're doing
# and want custom functionality.

# Exclusively used for video generation.

from input_parameters import quote, author, vid_output_name, imgGenre, random, audio, manual_audio
from util import select_audio

input_dict = {
  "quote": quote,
  "author": author,
  "outputName": vid_output_name,
  "font": "fonts/font.ttf",
  "audio": audio if manual_audio else "audios/" + select_audio(quote),
  "imagesPath": "./images/images" + str(imgGenre),
  "random": random,
  "bg_img_opacity": 0.2,
  "bg_img_duration": 0.5,
}