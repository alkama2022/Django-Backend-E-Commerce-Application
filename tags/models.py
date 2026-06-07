from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.

class Tag(models.Model):
    label = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.label


class TaggedItem(models.Model):
   # what tag applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # type of the tagged object
    # ID of the tagged object
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')