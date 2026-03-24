# 🎬 Quote Video Generator

A simple and customizable **quote video generator** that creates MP4 videos from configurable quote data.

<p align="center">
  <img src="example.gif" alt="Demo" width="300" />
</p>
(The background looks cursed because of being converted into a GIF, the produced video will not have this problem)

---

## Overview

This project generates a video as shown in the above GIF of 9:16 aspect ratio and automatically publishes it to Instagram using Github as a data storage. It also allows you to create an image quote as well. In `src/input_parameters.py` you can edit all parameters of the video / image, they are:

- `quote`: The actual quote.
- `author`: Author of the quote.

Other options for video generation are available to be edited as well but a little more technical. View them inside `src/input_parameters.py` and `src/input.py`. The audio is chosen by gemini api from the `audios/` folder. The `images/` folder contains subdirectories of images categorized by different genres. You can choose the subfolder yourself or use the `random` variable to randomly select from all subfolders with regex `images[0-9]*/*`.

All variables from `input_parameters.py` are passed to the file `input.py` which is then used by the `VideoGenerator` class. They are separated for ease of use and most of your time using this program will be spent inside the parameters file. In case you want custom functionality, you can directly edit the `input_dict` inside `input.py`

## Usage

### Setup

All libraries used and required are present in the `requirements.txt` file. Run the following commands to setup your environment:

```Py
python -m venv venv
source venv/source/activate # Or venv\Scripts\activate for windows
pip install -r requirements.txt
```

### Video Generation

You will need a gemini api key inside your `.env` so that a background audio can be chosen automatically. But if you don't want that, set the `manual_audio` variable to true inside `src/input_parameters.py`

Once the environment is setup, configure the parameters in `src/input_parameters.py` and run the `src/vid_generator.py` file to generate the video.

### Image Generation

You will need to specify a legitimate E-mail inside your .env as variable name: `WIKI_HEADER_EMAIL`. This is used in the headers when fetching the author image from wikipedia.

After that, simply configure the parameters in `src/input_parameters.py` to your liking and run the `src/img_generator.py` file to generate the image.

### Publishing

To publish the video, you'll have to get the following things and put them in your `.env`. An example .env file is present: `.env.example`. The parameters required are:

- `ACCESS_TOKEN`: The facebook GraphAPI access token.
- `BUSINESS_ACC_ID`: The business instagram account id.
- `GITHUB_PAT`: Github Personal Access Token.
- `GITHUB_REPO_PATH`: The github api link to the repository where the videos are stored.
- `GEMINI_API_KEY`: The Gemini API Key.

To get the access token and business account id, follow this Youtube video: https://www.youtube.com/watch?v=BuF9g9_QC04. I doubt anyone can actually get it from just the documentation, it's rubbish.

Github is used because the Facebook GraphAPI, as far as I can tell from whatever the hell their documentation is, doesn't allow direct uploads from the API. So you need to store it elsewhere and give them the link. Github I found to be a free option, but its sketchy at times. If you're willing to pay a little, Uploadcare is better.

After setup, running the `publisher.py` file will publish the image / video to Instagram.

## Contributing

The actual code is to be found in the `src/` folder. Its folder structure is as follows:

- `vid_generator.py`: Contains the `VideoGenerator` class. Running it after configuring `input_parameters.py` shall generate the video.
- `img_generator.py`: Contains the `ImageGenerator` class. Running it after configuring `input_parameters.py` shall generate the image.
- `input.py`: The input for video / image
- `publisher.py`: Contains `Publisher` class. Running it after after configuring `input_parameters.py` shall publish the video / image.
- `util.py`: Contains util functions

As a developer, you'll mainly be working in the `vid_generator.py`, `img_generator.py`, and `publisher.py` files. I got exams and am too lazy to implement tests, so just run edge cases yourself.

### Future changes

Here are some features I wanna add in the future:

- [ ] Hook up the quotes to some API
- [x] Use some AI to choose which audios would be best for a quote
- [ ] Add more images. They can be of any size since the `VideoGenerator` class does resize them, but it sometimes bugs out.
- [ ] On that topic, actually fixing why the `crop_image` function inside the `VideoGenerator` class bugs out and fixing it would be great lmao.
- [ ] Add different formats. Currently its just image shuffling. Other quotes formats involving fading transitions, or other variations.
- [x] Add image generation support

## License

This project has the MIT License. See `LICENSE` for more info.

## Author

I made this because I drank coffee at 2am and didn't want to study Physics xD.

Check out my website: https://sajawalhassan.vercel.app
