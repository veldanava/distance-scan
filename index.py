# install jangan lupa
import numpy as np
import cv2

# scan jarak antara objek dan kamera
# github.com/veldanava
# run: python index.py

# mark objek
def find_marker(image):
	# convert ke filter grayscale untuk mendeteksi setiap sisi
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = cv2.Canny(gray, 35, 125)
	(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	c = max(cnts, key = cv2.contourArea)
	# compute bounding box
	return cv2.minAreaRect(c)

# jarak ke kamera
def distance_to_camera(knownWidth, focalLength, perWidth):
	return (knownWidth * focalLength) / perWidth

# init jarak kamera ke objek
KNOWN_DISTANCE = 24.0

# init jarak objek yang tertangkap
KNOWN_WIDTH = 11.0

# contoh
IMAGE_PATHS = ["images/city.jpg"]

# load objek trus scan jaraknya
image = cv2.imread(IMAGE_PATHS[0])
marker = find_marker(image)
focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH

# loop
for imagePath in IMAGE_PATHS:
	# load objek trus kasih tanda pake marker
	image = cv2.imread(imagePath)
	marker = find_marker(image)
	inches = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])

	# display
	box = np.intp(cv2.boxPoints(marker))
	cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
	cv2.putText(image, "%.2fmeter" % (inches / 12),
		(image.shape[1] - 200, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
		2.0, (0, 255, 0), 3)
	cv2.imshow("hasil scan jarak", image)
	cv2.waitKey(0)
