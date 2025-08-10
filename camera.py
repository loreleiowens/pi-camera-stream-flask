#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This scrtipt script..

import cv2 as cv
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
import time
from datetime import datetime
import numpy as np

class VideoCamera(object):
    def __init__(self, flip = False, file_type  = ".jpg", photo_string= "stream_photo"):
        # self.vs = PiVideoStream(resolution=(1920, 1080), framerate=30).start()
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration({'format': 'RGB888'}))
        self.picam2.start()
        self.flip = flip # Flip frame vertically
        self.file_type = file_type # image type i.e. .jpg
        self.photo_string = photo_string # Name to save the photo
        time.sleep(2.0)

    def __del__(self):
        self.picam2.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        frame = self.picam2.capture_array()
        frame = self.flip_if_needed(frame)
        ret, jpeg = cv.imencode(self.file_type, frame)
        self.previous_frame = jpeg
        return jpeg.tobytes()

    # Take a photo, called by camera button
    def take_picture(self):
        frame = self.picam2.capture_array()
        frame = self.flip_if_needed(frame)
        ret, image = cv.imencode(self.file_type, frame)
        today_date = datetime.now().strftime("%m%d%Y-%H%M%S") # get current time
        cv.imwrite(str(self.photo_string + "_" + today_date + self.file_type), frame)
    
    def take_video(self):
        video_config = self.picam2.create_video_configuration()
        self.picam2.configure(video_config)
        encoder = H264Encoder(bitrate=10000000)
        today_date = datetime.now().strftime("%m%d%Y-%H%M%S") # get current time
        output = str(self.photo_string + "-" + today_date)
        self.picam2.start_recording(encoder, output)
    
    def stop_video(self):
        self.picam2.stop_recording()

