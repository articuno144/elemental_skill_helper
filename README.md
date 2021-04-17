# [Genshin Impact] Elemental skill helper
A helper script to keep track of the elemental skill cooldowns.

## Dependencies
'pip install numpy Pillow opencv-python pytesseract mss==2.0.22'

## How to config
If you are using Mona in your team, in `config.json`, change the value next to "mona" to her position in the team (1,2,3,4). Otherwise, set it to 0. She is special because of her dodge.

This script is tested under the screen resolution of 1920×1080. For other resolutions, you need to change the bounding box corner positions in the config files accordingly.

## How to use
Just double click on `skill_helper.py` and run your game in full screen in the left-most monitor (subject to your own config).
