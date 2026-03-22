from util import select_audio

# Edit these variables as a user, edit dict if you know what you're doing.

quote = """ “When liberty exceeds intelligence, it begets chaos, which begets dictatorship.” """
outputName = "output.mp4" # video gen
# outputName = "output.png" # image gen
author = "Will Durant"
audio = select_audio(quote)

input_dict = {
  "quote": quote,
  "author": author,
  "outputName": outputName,
  "font": "fonts/font.ttf",
  "audio": "audios/" + audio,
  "imagesPath": "./images/images2",
  "random": True,
  "bg_img_opacity": 0.2,
  "bg_img_duration": 0.3,

  "file_path": outputName
}