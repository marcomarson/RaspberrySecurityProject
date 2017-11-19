from picamera import PiCamera
import time

class Camera():
    def __init__(self):
        self.camera=PiCamera()

    def tirafoto(self, ap):
        self.camera.start_preview()
        time.sleep(3)
        self.camera.capture('/home/pi/PhotosMAM/'+ap+'-%d_%m_%y-%H%M%S.jpg')
        self.camera.stop_preview()

    def fecha(self):
        self.camera.close()
