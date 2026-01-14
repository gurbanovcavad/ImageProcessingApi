import numpy as np
import cv2

class RotationService:
    def run(self, image, params):
        angle = params.get("angle")
        h, w = image.shape[:2]
        center = (w // 2, h // 2)
        mat = cv2.getRotationMatrix2D(center, angle, 1)
        cos = np.abs(mat[0, 0])
        sin = np.abs(mat[0, 1])
        new_w = int((h * sin) + (w * cos))
        new_h = int((h * cos) + (w * sin))
        mat[0, 2] += (new_w / 2) - center[0]
        mat[1, 2] += (new_h / 2) - center[1]
        rotated_image = cv2.warpAffine(image, mat, (new_w, new_h), borderMode=cv2.BORDER_CONSTANT, borderValue=(255,255,255))
        return rotated_image, None
    
    def validate(self, params, w = None, h = None):
        angle = params.get("angle")
        if angle == None:
            raise Exception("Invalid Rotation Parameters")