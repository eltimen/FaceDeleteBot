# FaceDeleteBot
Simple Telegram bot for blur faces on image

![](example.jpg)

# Installation
Python 3.7 or above required
1. Install dependencies: `pip install numpy dlib opencv-python imutils telepot`
2. Download `shape_predictor_68_face_landmarks.dat.bz2` from [link](https://github.com/davisking/dlib-models/raw/master/shape_predictor_68_face_landmarks.dat.bz2) and extract it to `models/` folder
3. Place your Telegram bot token in `token.txt` file
4. Use:
	* `python bot.py` to run bot 
	* `python engine.py test_images/lena.png` for local demo

# TODOs
* Improve face detection algorithm (see tests `band.jpg` and `tilted_face.jpg`). Possible way is use OpenCV to find face rectangles and after proccess it via dlib.
* Improve performance under large number of queries
* Add support photo sended as file
* Add support of multiple photos in one message