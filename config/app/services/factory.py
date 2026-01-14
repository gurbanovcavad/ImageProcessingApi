from .resize import ResizeService
from .rotate import RotationService
from .grayscale import GrayscaleService
from .convert_channel import ChannelConversionService
from .perspective_transformation import PerspectiveService
from .compress import CompressionService
from .convert_format import FormatConversionService
from .draw import DrawService
from .generate_gif import GifGenerationService

class ServiceFactory:
    def __init__(self):
        self.resize_service = ResizeService()
        self.rotation_service = RotationService()
        self.grayscale_service = GrayscaleService()
        self.channel_conversion_service = ChannelConversionService()
        self.perspective_service = PerspectiveService()
        self.compression_service = CompressionService()
        self.format_conversion_service = FormatConversionService()
        self.draw_service = DrawService()
        self.gif_generation_service = GifGenerationService()
        
service_factory = ServiceFactory()