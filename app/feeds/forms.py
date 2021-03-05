from django.forms import ModelForm

from cloudinary.forms import CloudinaryJsFileField, CloudinaryUnsignedJsFileField
# Next two lines are only used for generating the upload preset sample name
from cloudinary.compat import to_bytes
import cloudinary, hashlib
from .models import Photo
from .models import Feed
"""
class PhotoDirectForm(forms.ModelForm):
  class Meta:
      model = Photo
  image = CloudinaryJsFileField()
  """
class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = '__all__'

class PhotoDirectForm(PhotoForm):
    image = CloudinaryJsFileField()

class EditPostForm(ModelForm):
    class Meta:
        model = Feed
        fields = ('post',)
