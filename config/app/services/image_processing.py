from ninja.errors import HttpError
from .factory import service_factory
import numpy as np
import cv2, base64
from ..models import ImageArtifact, FilePath
import io
from PIL import Image

class ImageProcessingService:
    def __init__(self):
        self.resize_service = service_factory.resize_service
        self.rotation_service = service_factory.rotation_service
        self.grayscale_service = service_factory.grayscale_service
        self.channel_conversion_service = service_factory.channel_conversion_service
        self.perspective_service = service_factory.perspective_service
        self.compression_service = service_factory.compression_service
        self.format_conversion_service = service_factory.format_conversion_service
        self.draw_service = service_factory.draw_service
        self.gif_generation_service = service_factory.gif_generation_service
        
        self.services = {
            "resize": self.resize_service,
            "rotate": self.rotation_service,
            "grayscale": self.grayscale_service,
            "channel_conversion": self.channel_conversion_service,
            "perspective_transformation": self.perspective_service,
            "compress": self.compression_service,
            "format_conversion": self.format_conversion_service,
            "draw": self.draw_service
        }
        
    # validate provided operation
    def validate(self, operation):
        # operation type
        op = operation.operation
        if not op:
            raise Exception("Operation Type Should be Provided")
        op = op.lower()
        service = self.services.get(op)
        if not op:
            raise Exception("Unsupported Operation")
        return service
    
    # perform manipulation operations
    def apply(self, data, format, operations, request, extensions = None):
        try:
            pipeline = []
            # storage mode
            database = False
            success = False
            fail = False
            gif = False
            frame_interval = None
            if format == 'f':
                if operations.gif:
                    gif = (operations.gif.generate if operations.gif.generate else False)
                if operations.storage == 'database':
                    database = True
                if gif:
                    frame_interval = operations.gif.frame_interval
                images = self.convert_files(data)
                for i in operations.operations:
                    pipeline.append(i.directives)
            else:
                # holds base64 strings and their corresponding operations 
                temp = data.images
                if data.gif:
                    gif = (data.gif.generate if data.gif.generate else False)
                if data.storage == 'database':
                    database = True
                if gif:
                    frame_interval = data.gif.frame_interval
                images, extensions = self.decode_base64(temp)
                for i in temp:
                    pipeline.append(i.directives)
            input_path = "/images/input/"
            output_path = "/images/output/"
            service = None
            outputs = []
            output = []
            error = ""
            if len(images) != len(pipeline):
                raise Exception("The Numbers of Images and Operations don't Match")
            for i, image in enumerate(images):
                input_filename = str(request.id) + "-" + str(i)
                input_extension = extensions[i]
                input_file_path = FilePath.objects.create(directory=input_path, filename=input_filename, extension=input_extension, storage_key=input_path+input_filename+"."+input_extension)
                input_image = ImageArtifact.objects.create(request=request, role="input", file_path=input_file_path)
                cv2.imwrite(input_path + input_filename + "." + input_extension, image)
                output = image
                # to check if the operations succeeded on the images[i] 
                ok = True
                
                for j, operation in enumerate(pipeline[i]):
                    h, w = image.shape[:2] 
                    try:
                        service = self.validate(operation)
                        service.validate(operation.parameters, w, h)
                    except Exception as e:
                        error = str(e)
                        fail = True
                        ok = False
                        break
                
                if not ok:
                    continue
                format = extensions[i]
                for j, operation in enumerate(pipeline[i]):
                    service = self.validate(operation)
                    try:
                        output, new_format = service.run(output, operation.parameters)
                        if new_format != None:
                            format = new_format
                    except Exception as e:
                        error = str(e)
                        fail = True
                        ok = False
                        break
                if not ok:
                   continue 
               
                try: 
                    output_filename = str(request.id) + "-" + str(i)
                    output_extension = format
                    output_file_path = FilePath.objects.create(directory=output_path, filename=output_filename, extension=output_extension, storage_key=output_path+output_filename+"."+output_extension)
                    output_image = ImageArtifact.objects.create(request=request, role="output", file_path=output_file_path)
                    
                    if database:
                        suc, buffer = cv2.imencode("." + output_extension, output)
                        
                        if not suc:
                            raise Exception("Failed to Encode Image to Base64 string")
                        image_base64 = base64.b64encode(buffer).decode("utf-8")
                        output_image.base64_data = image_base64
                        output_image.save()

                    outputs.append(output_path + output_filename + "." + output_extension)
                    cv2.imwrite(output_path + output_filename + "." + output_extension, output)
                except Exception as e:
                    fail = True
                    ok = False
                    error = str(e)
                if ok: 
                    success = True

            if gif and len(images) > 1:
                try:
                    gif_name = self.gif_generation_service.run(images, frame_interval, str(output_path) + str(request.id))
                    outputs.append(gif_name)
                except Exception as e:
                    error = str(e)
                    ok = False
                    fail = True
            elif gif and len(images) < 2:
                ok = False
                fail = True
                
            if ok:
                success = True
            status = ""
            if fail and success:
                status = "partial success"
            elif fail:
                status = "fail"
            else:
                status = "success" 
            
            return outputs, status, error
        except Exception as e:
            return [], "fail", str(e) 

    # convert files to images
    def convert_files(self, images):
        res = []
        for image in images:
            np_data = np.frombuffer(image, np.uint8)
            image = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
            res.append(image)
        return res

    # decode base64 strings to byte
    def decode_base64(self, images):
        res = []
        extensions = []
        for img in images:
            temp = img.data
            base64_data = temp.split(",")[1] if "," in temp else temp 
            image_data = base64.b64decode(base64_data)
            image = Image.open(io.BytesIO(image_data))
            extensions.append(image.format.lower())
            np_data = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
            res.append(image)
        return res, extensions
    
    def get(self, path: str):
        try:
            format = path[-3:]
            if format == "gif":
                with open(path, "rb") as gif:
                    res = base64.b64encode(gif.read()).decode('utf-8')
                
                    return res
                
            format = ("jpeg" if format == "jpg" else format)
            image = Image.open(path)
            buffer = io.BytesIO()
            image.save(buffer, format=format.upper())
            res = base64.b64encode(buffer.getvalue()).decode('utf-8')
            return res
        except Exception as e:
            raise HttpError(404, "Image is not Found")