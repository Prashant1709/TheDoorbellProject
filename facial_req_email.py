#! /usr/bin/python

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2
from gtts import gTTS
import requests
import os
import math

#Initialize 'currentname' to trigger only when a new person is identified.
currentname = "unknown"
#Determine faces from encodings.pickle file model created from train_model.py
encodingsP = "encodings.pickle"
#use this xml file
cascade = "haarcascade_frontalface_default.xml"
#function to announce
API_Key = "your_key_here"
location = "Bhubaneswar"
weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid="
final_url = weather_url + API_Key
def weather_dat():
	weather_data = requests.get(final_url).json()
	y=weather_data['main']
	z=weather_data['wind']
	speed=z['speed']
	current_te=y['temp']-273
	current_hu=y['humidity']
	math.floor(current_te)
	#pprint(math.floor(current_te))
	#pprint(current_hu)
	#pprint(speed)
	mytext = 'The Temperature outside is'+str(math.floor(current_te))+'degree celsius.The Humidity is'+str(current_hu)+'percent.The wind speed is'+str(speed)+'kilometer per hour. '
	play_sound(mytext)
def play_sound(data):
    mytext = data
    language = 'en'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("welcome.mp3")
    os.system("mpg321 welcome.mp3")
#function for setting up emails
def send_message(name):
    return requests.post(
        "https://api.mailgun.net/v3/sandbox2e1c6c47d3b845f798ad34bed12bdb16.mailgun.org/messages",
        auth=("api", "7467768c0af11c89e382c3a8a35b71cd-eb38c18d-3059504b"),
        files = [("attachment", ("image.jpg", open("image.jpg", "rb").read()))],
        data={"from": 'mailgun@sandbox2e1c6c47d3b845f798ad34bed12bdb16.mailgun.org',
            "to": ["upadhyay.prashant001@gmail.com"],
            "subject": "You have a visitor",
            "html": "<html>" + name + " is at your door.  </html>"})

# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
#print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(encodingsP, "rb").read())
detector = cv2.CascadeClassifier(cascade)

# initialize the video stream and allow the camera sensor to warm up
#print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
i=0
# start the FPS counter
fps = FPS().start()

# loop over frames from the video file stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to 500px (to speedup processing)
	frame = vs.read()
	frame = imutils.resize(frame, width=500)
	
	# convert the input frame from (1) BGR to grayscale (for face
	# detection) and (2) from BGR to RGB (for face recognition)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	# detect faces in the grayscale frame
	rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
		minNeighbors=5, minSize=(30, 30),
		flags=cv2.CASCADE_SCALE_IMAGE)

	# OpenCV returns bounding box coordinates in (x, y, w, h) order
	# but we need them in (top, right, bottom, left) order, so we
	# need to do a bit of reordering
	boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

	# compute the facial embeddings for each face bounding box
	encodings = face_recognition.face_encodings(rgb, boxes)
	names = []

	# loop over the facial embeddings
	for encoding in encodings:
		# attempt to match each face in the input image to our known
		# encodings
		matches = face_recognition.compare_faces(data["encodings"],
			encoding)
		name = "Unknown"

		# check to see if we have found a match
		if True in matches:
			# find the indexes of all matched faces then initialize a
			# dictionary to count the total number of times each face
			# was matched
			matchedIdxs = [i for (i, b) in enumerate(matches) if b]
			counts = {}

			# loop over the matched indexes and maintain a count for
			# each recognized face face
			for i in matchedIdxs:
				name = data["names"][i]
				counts[name] = counts.get(name, 0) + 1

			# determine the recognized face with the largest number
			# of votes (note: in the event of an unlikely tie Python
			# will select first entry in the dictionary)
			name = max(counts, key=counts.get)
			
			#If someone in your dataset is identified, print their name on the screen
			if currentname != name:
				currentname = name
				print(currentname)
				#Take a picture to send in the email
				img_name = "image.jpg"
				cv2.imwrite(img_name, frame)
				print('Taking a picture.')
				i=i+1
				#Now send me an email to let me know who is at the door
				request = send_message(name)
				print ('Status Code: '+format(request.status_code)) #200 status code means email sent successfully
				play_sound('Welcome Home'+name+'.')
				weather_dat()
		# update the list of names
		names.append(name)

	# loop over the recognized faces

	# display the image to our screen
	#cv2.imshow("Facial Recognition is Running", frame)
	#key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	#if key == ord("q"):
	if i==0:
		print("No Match Found")

	# update the FPS counter
	fps.update()
	#print("fps updated")
	break

# stop the timer and display FPS information
fps.stop()
#print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
#print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
