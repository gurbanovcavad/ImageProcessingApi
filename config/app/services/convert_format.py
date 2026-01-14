SUPPORTED_FORMATS = ["jpg", "png", "PNG", "JPEG", "JPG", "jpeg"]

class FormatConversionService:
    def run(self, image, params):
        target = params.get("target").lower()
        return image, target
    
    def validate(self, params, w = None, h = None):
        target = params.get("target")
        if target == None or target not in SUPPORTED_FORMATS:
            raise Exception("Invalid Format Conversion Parameters")