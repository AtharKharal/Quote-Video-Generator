# For normal usage, just edit these variables to your liking.
# If you know what you're doing, you can also directly edit the `input_dict` inside `input.py`

from util import get_random_quote

quote_manual = """“Some care is needed in using Descartes' argument. "I think, therefore I am" says rather more than is strictly certain. It might seem as though we are quite sure of being the same person to-day as we were yesterday, and this is no doubt true in some sense. But the real Self is as hard to arrive at as the real table, and does not seem to have that absolute, convincing certainty that belongs to particular experiences.” """
author_manual = "Bertrand Russell, The Problems of Philosophy "
autogen_quote = True


vid_output_name = "output.mp4"
img_output_name = "output.png"


# --- Video Generation ---
imgGenre = 1 # Subfolder no. Is useless if `random` is set to true
random = True
audio = "audios/10.mp3"
manual_audio = False # Manually point to audio file instead of having gemini select it.


if autogen_quote == True: quote_gen, author_gen = get_random_quote()
quote = quote_gen if autogen_quote else quote_manual
author = author_gen if autogen_quote else author_manual