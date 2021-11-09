import argparse
import sys
import time
import json
import signal
import os

import cv2
from object_detector import ObjectDetector
from object_detector import ObjectDetectorOptions
import utils

def run(model: str, camera_id: int, width: int, height: int, num_threads: int, enable_edgetpu: bool) -> None:
    # start capturing video input from the camera
    #cap = cv2.VideoCapture(camera_id)
    cap = cv2.VideoCapture('video.mp4')
    #cap = cv2.VideoCapture('/dev/video0')
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # Initialize the object detection model
    options = ObjectDetectorOptions(num_threads=num_threads, score_threshold=0.3, max_results=3, enable_edgetpu=enable_edgetpu)
    detector = ObjectDetector(model_path=model, options=options)

    # continuously capture images from the camera and run inference
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            sys.exit('ERROR: Unable to read from webcam. Please verify your webcam settings.')

        image = cv2.flip(image, 1)
        detections = detector.detect(image)
        
        for detection in detections:
            category = detection.categories[0]
            class_name = category.label
            probability = round(category.score, 2)
            printjson("detected", {"object": class_name})

        if cv2.waitKey(1) == 27:
          break

    cap.release()
    cv2.destroyAllWindows()
  

def printjson(type, message):
	print(json.dumps({type: message}))
	sys.stdout.flush()

def signalHandler(signal, frame):
	global closeSafe
	closeSafe = True


def main():
    signal.signal(signal.SIGINT, signalHandler)
    closeSafe = False
    
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--model', help='Path of the object detection model.', required=False, default='efficientdet_lite0.tflite')
    parser.add_argument('--cameraId', help='Id of camera.', required=False, type=int, default=0)
    parser.add_argument('--frameWidth', help='Width of frame to capture from camera.', required=False, type=int, default=640)
    parser.add_argument('--frameHeight', help='Height of frame to capture from camera.', required=False, type=int, default=480)
    parser.add_argument('--numThreads', help='Number of CPU threads to run the model.', required=False, type=int, default=4)
    parser.add_argument('--enableEdgeTPU', help='Whether to run the model on EdgeTPU.', action='store_true', required=False, default=False)
    args = parser.parse_args()

    run(args.model, int(args.cameraId), args.frameWidth, args.frameHeight, int(args.numThreads), bool(args.enableEdgeTPU))

if __name__ == '__main__':
    main()