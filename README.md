# FaceDeleteBot
Simple Telegram bot for blurring faces on the image

![](example.jpg)

# Installation
Python 3.7 or above required
1. Install dependencies: `pip install -r requirements.txt`
2. Download `shape_predictor_68_face_landmarks.dat.bz2` [here](https://github.com/davisking/dlib-models/raw/master/shape_predictor_68_face_landmarks.dat.bz2) and extract it to `models/` folder
3. Place your Telegram bot token in the `token.txt` file
4. Use:
	* `python bot.py` to run bot 
	* `python engine.py test_images/lena.png` to test engine locally on a some demo

# TODOs
* Improve face detection algorithm (see tests `band.jpg` and `tilted_face.jpg`). Possible ways:
  * use OpenCV to find face rectangles and post-process them via dlib
  * or just use some deep learning techniques 
* Improve performance under large number of queries