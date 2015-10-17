from rest_framework import serializers

from .models import PrivateMessage
from .models import Profile
from .models import PublicMessage

class PrivateMessageSerializer(serializers.ModelSerializer):
    class Meta:
       model = PrivateMessage
       fields = ('text', 'createdby', 'receives', 'mytime')
       
class PublicMessageSerializer(serializers.ModelSerializer):
    class Meta:
       model = PublicMessage
       fields = ('text', 'createdby', 'receives', 'mytime')
       
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
       model = Profile
       fields = ('text', )