from django.db import models
import uuid 

STATUS_CHOICES = [("success", "Success"), ("partial success", "Partial Success"), ("fail", "Fail")]
ROLE_CHOICES = [("input", "Input"), ("output", "Output")]

class FilePath(models.Model):
    directory = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    extension = models.CharField(max_length=255)
    storage_key = models.CharField(max_length=255)

class JsonPayload(models.Model):
    json_payload = models.JSONField()

class Request(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    user_ip = models.GenericIPAddressField()
    status = models.CharField(max_length=25, choices=STATUS_CHOICES)
    error = models.TextField(null=True, blank=False)
    payload = models.ForeignKey(JsonPayload, null=True, blank=True, on_delete=models.SET_NULL, related_name="payload")
    
    class Meta:
        indexes = [
            models.Index(fields=["timestamp"]),
            models.Index(fields=["user_ip"]),
            models.Index(fields=["status"]),
        ]
    
class ImageArtifact(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name="images")
    # input or output
    role = models.CharField(max_length=25, choices=ROLE_CHOICES)
    file_path = models.ForeignKey(FilePath, null=True, blank=False, on_delete=models.SET_NULL, related_name="path")
    base64_data = models.TextField(null=True, blank=False)