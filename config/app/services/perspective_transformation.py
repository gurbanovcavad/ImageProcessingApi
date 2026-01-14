import numpy as np
import cv2

class PerspectiveService:
    def run(self, image, params):
        h, w = image.shape[:2]      
        source = params.get("source")
        des = params.get("destination")
        src = np.array(source, np.float32)
        dst = np.array(des, dtype=np.float32)
        # for i in range(4):    
        #     cv2.circle(image, source[i], 5, (0,0,255), -1)
        #     cv2.circle(image, des[i], 5, (255,0,0), -1)
            
        matrix = cv2.getPerspectiveTransform(src, dst)
        transformed_image = cv2.warpPerspective(image, matrix, (w, h))
        return transformed_image, None
    
    def validate(self, params, w = None, h = None):
        src = params.get("source")
        dst = params.get("destination")
        if src == None or dst == None:
            raise Exception("Invalid Perspective Transformation Parameters")
        for i in range(4):
            if src[i][0] < 0 or src[i][1] < 0 or src[i][0] > w or src[i][1] > h: 
                raise Exception("Invalid Perspective Transformation Parameters")
            if dst[i][0] < 0 or dst[i][1] < 0 or dst[i][0] > w or dst[i][1] > h: 
                raise Exception("Invalid Perspective Transformation Parameters")