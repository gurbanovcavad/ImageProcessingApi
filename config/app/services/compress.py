import cv2

class CompressionService:
    def run(self, image, params):
        quality = params.get("quality")
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        _, encoded_img = cv2.imencode('.jpg', image, encode_param)
        decoded_img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
        
        return decoded_img, None
    
    def validate(self, params, w = None, h = None):
        quality = params.get("quality")
        if quality == None or quality < 0:
            raise Exception("Invalid Compression Parameters")