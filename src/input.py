from captions import captions, follow_text

quote = """Pain and suffering are always inevitable for a large intelligence and a deep heart. The really great men must, I think, have great sadness on earth."""
outputName = "vid_to_be_published2.mp4"

input_dict = {
  "quote": quote,
  "author": "Fyodor Dostoevsky",
  "outputName": outputName,
  "font": "fonts/font.ttf",
  "audio": "audios/4.mp3",
  "imagesPath": "./images/images1",
  "random": False,
  "bg_img_opacity": 0.2,
  "bg_img_duration": 0.25,

  "caption": f"""{quote}\n\n{follow_text}\n\n{captions["Fyodor Dostoevsky"]}""",
  "file_path": outputName
}