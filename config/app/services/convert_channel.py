import cv2

SUPPORTED_CHANNELS = ["rgb", "bgr", "RGB", "BGR"]
BGR = ["BGR", "bgr"]

class ChannelConversionService:
    def run(self, image, params):
        to = params.get("to")
        res = None
        if to in BGR:
            res = self.to_bgr(image)
        else:
            res = self.to_rgb(image)
        return res, None

    def validate(self, params, w = None, h = None):
        channel = params.get("channel")
        to = params.get("to")
        if channel not in SUPPORTED_CHANNELS or to not in SUPPORTED_CHANNELS:
            raise Exception("Invalid Channel Conversion Parameters") 

    def to_rgb(self, image):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return rgb_image
        
    def to_bgr(self, image):
        bgr_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        return bgr_image