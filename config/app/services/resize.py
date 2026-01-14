import cv2

class ResizeService:
    def run(self, image, params):
        mode = params.get("mode")
        width = params.get("width")
        height = params.get("height")
        h, w = image.shape[:2]
        if mode == "exact" or not mode:
            resized_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)
        elif mode == "preserve_aspect":
            # resizing by provided height, while preserving the aspect ratio
            if height and not width:
                scale = height / h
                new_w = w * scale
                resized_image = cv2.resize(image, (new_w, height), interpolation=cv2.INTER_LINEAR)
            # resizing by provided width, while preserving the aspect ratio
            else:
                scale = width / w
                new_h = h * scale
                resized_image = cv2.resize(image, (width, new_h), interpolation=cv2.INTER_LINEAR)
        else:
            raise Exception("Invalid Mode")
        return resized_image, None
    
    def validate(self, params, w = None, h = None):
        mode = params.get("mode")
        width = params.get("width")
        height = params.get("height")
        if (mode == "exact" or not mode) and (not width or not height):
            raise Exception("Invalid Resize Parameters") 
        if mode == "preserve_aspect" and ((not width and not height) or (width and height)):
            raise Exception("Invalid Resize Parameters")