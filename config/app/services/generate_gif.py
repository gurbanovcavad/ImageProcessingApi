import cv2
from PIL import Image

class GifGenerationService:
    def run(self, images, frame_interval, name):
        if frame_interval == None or frame_interval <= 0:
            raise Exception("Invalid Gif Parameters")
        duration = int(frame_interval * 1000)
        gif = self.cv2_to_pil(images)
        name += ".gif"
        gif[0].save(name, save_all=True, append_images=gif[1:], duration=duration, loop=0, optimize=False)
        return name

    def cv2_to_pil(self, images):
        max_h = max(img.shape[0] for img in images)
        max_w = max(img.shape[1] for img in images)

        pil_images = []
        for img in images:
            padded = cv2.resize(img, (max_w, max_h), interpolation=cv2.INTER_LINEAR)
            img_rgb = cv2.cvtColor(padded, cv2.COLOR_BGR2RGB)
            pil_images.append(Image.fromarray(img_rgb))
        
        return pil_images