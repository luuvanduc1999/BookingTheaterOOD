from rest_framework import serializers
from system.models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "title", "content")
    
    def to_representation(self, instance): 
        data = super().to_representation(instance)
        return data
    