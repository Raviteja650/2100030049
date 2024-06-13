from rest_framework import serializers

from . models import Numbers

class numberSerializer(serializers.ModelSerializer):
    class Meta:
        model=Numbers
        fields=['id','value']
    
