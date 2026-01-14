from ninja_extra import ControllerBase, api_controller, http_post, http_get
from ..services.image_processing import ImageProcessingService
from django.http import HttpRequest
from ninja.errors import HttpError
from ..schemas import Base64Format, FormFormat
from typing import Optional, List
from ninja import File
from ninja.files import UploadedFile
import json
from ..models import Request, JsonPayload

@api_controller('/images', tags='Image Operations')
class ImageProcessingController(ControllerBase):
    def __init__(self, service: ImageProcessingService):
        self.service = service

    @http_post('/process')
    def process_images(self, request: HttpRequest, images: Optional[List[UploadedFile]] = File(None)):
        try:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')
            format = "f"
            # to check if the request in the form format 
            ok = False
            # form format
            if request.POST.get('operations'):
                ok = True
                temp = json.loads(request.POST['operations'])
                extensions = [image.name[-3:] for image in images]
                form_operations = FormFormat(storage=temp.get("storage"),operations=temp.get("operations"), gif=temp.get("gif"))
                data = [file.read() for file in images]
            # base64 format
            elif request.body:
                temp = json.loads(request.body)
                data = Base64Format(images=temp.get("images"),storage=temp.get("storage"), gif=temp.get("gif"))
                extensions = []
                format = "b"
            else:
                raise HttpError(400, "Invalid Request")
            try:
                payload = JsonPayload.objects.create(json_payload=temp)
                req = Request.objects.create(user_ip=ip, payload=payload)
                outputs, status, error = self.service.apply(data, format, form_operations if ok else None, req, extensions)
                req.status = status 
                req.error = error
                req.save()
            except Exception as e:
                raise Exception("Failed to Log the Request")
            return {
                "request_id": req.id,
                "outputs": outputs,
                "status": status,
                "message": error
                } 
        except Exception as e:
            raise HttpError(400, str(e))
        
    @http_get("/")
    def get_image(self, request: HttpRequest, path: str):
        return self.service.get(path)