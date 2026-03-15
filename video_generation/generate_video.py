from vid_generator import VideoGenerator

input_dict = {
  "quote": "Darken your room, shut the door, empty your mind. You are still in great company.",
  "author": "A.O. Spare",
  "outputName": "output.mp4",
  "font": "fonts/font.ttf",
  "audio": "audios/audio.mp3"
}

vidGen = VideoGenerator(input_dict["quote"], input_dict["author"], input_dict["outputName"], input_dict["font"], input_dict["audio"])

def main():
    vidGen.generate()

if __name__ == "__main__":
    main()