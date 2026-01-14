from ninja_extra import NinjaExtraAPI
from .controllers.image_processing import ImageProcessingController
from .services.resize import ResizeService
from .services.rotate import RotationService
from .services.grayscale import GrayscaleService
from .services.convert_channel import ChannelConversionService
from .services.perspective_transformation import PerspectiveService
from .services.compress import CompressionService
from .services.convert_format import FormatConversionService
from .services.draw import DrawService
from .services.image_processing import ImageProcessingService


api = NinjaExtraAPI(title="Image Operations", version="0.1.0")

api.register_controllers(ImageProcessingController)