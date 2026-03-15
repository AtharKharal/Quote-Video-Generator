from vid_generator import VideoGenerator

input_dict = {
  "quote": "All the world's a stage, and all the men and women merely players",
  "author": "William Shakesphere",
  "outputName": "output.mp4",
  "font": "fonts/font.ttf",
  "audio": "audios/audio.mp3"
}

vidGen = VideoGenerator(input_dict["quote"], input_dict["author"], input_dict["outputName"], input_dict["font"], input_dict["audio"])

def main():
    vidGen.generate()

if __name__ == "__main__":
    main()