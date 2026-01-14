import cv2

class GrayscaleService:
    def run(self, image, params = None):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return gray_image, None
    
    def validate(self, params = None, w = None, h = None):
        pass