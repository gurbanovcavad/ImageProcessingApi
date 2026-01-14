from typing import Optional, List, Any
from ninja import Schema

class Operation(Schema):
    operation: str
    parameters: Optional[dict] = None

class ImageMetadata(Schema):
    filename: Optional[str] = None
    format: Optional[str] = None
    directives: Optional[List[Operation]] = None
    
class Image(ImageMetadata):
    data: str    
    
class GifParameters(Schema):
    generate: bool
    frame_interval: int
    
class Base64Format(Schema):
    storage: Optional[str]
    images: List[Image]
    gif: Optional[GifParameters] = None
    
class FormFormat(Schema):
    storage: Optional[str]
    gif: Optional[GifParameters] = None
    operations: List[ImageMetadata]