from picamera import PiCamera
import time

class Camera():
    def __init__(self):
        self.camera=PiCamera()

    def tirafoto(self, fotenha):
        self.camera.start_preview()
        time.sleep(3)
        self.camera.capture('/home/pi/projeto/'+fotenha)
        self.camera.stop_preview()

    def fecha(self):
        self.camera.close()

        
