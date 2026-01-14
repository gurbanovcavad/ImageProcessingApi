import cv2

TYPES = ["dots", "rectangles", "circles"]

class DrawService:
    """
        "operation": "draw",
        "parameters": {
            "dots": [
                {
                    "position": [x, y],
                    "color": [r, g, b]
                }
            ]
            
            "rectangles": [
                {
                    "position": [x, y],
                    "size": sz,
                    "color": [r, g, b],
                    "thickness": t
                }
            ]
            
            "circles": [
                {
                    "center": [x, y],
                    "radius": r,
                    "color": [r, g, b],
                    "thickness": t
                }
            ]
        }
    """
    def run(self, image, params):
        dots = params.get("dots")
        if dots != None:
            image = self.draw_dots(image, dots)
                
        rectangles = params.get("rectangles")
        if rectangles != None:
            image = self.draw_rectangles(image, rectangles)
                
        circles = params.get("circles")
        if circles != None:
           image = self.draw_circles(image, circles)
        
        return image, None
        
    def validate(self, params, w = None, h = None):
        # checks whether the parameters is empty
        bad = True
        dots = params.get("dots")
        if dots != None:
            bad = False
            for dot in dots:
                position = dot.get("position")
                color = dot.get("color")

                if len(position) != 2 or len(color) != 3:
                    raise Exception("Invalid Drawing Parameters")
                
        rectangles = params.get("rectangles")
        if rectangles != None:
            bad = False
            for rectangle in rectangles:
                position = rectangle.get("position")
                size = rectangle.get("size")
                thickness = rectangle.get("thickness")
                color = rectangle.get("color")
                
                if position == None or size == None or color == None or len(position) != 2 or len(size) != 2 or thickness == None or len(color) != 3:
                    raise Exception("Invalid Drawing Parameters")

        circles = params.get("circles")
            
        if circles != None:
            bad = False
            for circle in circles:
                center = circle.get("center")
                rad = circle.get("radius")
                thickness = circle.get("thickness")
                color = circle.get("color")
                
                if center == None or color == None or len(center) != 2 or rad == None or thickness == None or len(color) != 3:
                    raise Exception("Invalid Drawing Parameters")
        
        if bad:
            raise Exception("Invalid Drawing Parameters")
        
    def draw_dots(self, image, dots):
        for dot in dots:
            pos = dot.get("position")
            # bgr color 
            color = dot.get("color")
            rgb = [color[2], color[1], color[0]]
            image[pos[0], pos[1]] = rgb
        
        return image

    def draw_rectangles(self, image, rectangles):
        for rectangle in rectangles:
            position = rectangle.get("position")
            size = rectangle.get("size")
            thickness = rectangle.get("thickness")
            # bgr color
            color = rectangle.get("color")
            rgb = [color[2], color[1], color[0]]
            cv2.rectangle(image, position, (position[0] + size[0], position[1] - size[1]), rgb, thickness)
        return image
    
    def draw_circles(self, image, circles):
        for circle in circles:
            center = circle.get("center")
            rad = circle.get("radius")
            thickness = circle.get("thickness")
            # bgr color
            color = circle.get("color")
            
            rgb = [color[2], color[1], color[0]]
            cv2.circle(image, center, rad, rgb, thickness)
        return image