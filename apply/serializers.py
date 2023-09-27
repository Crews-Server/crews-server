from rest_framework import serializers
from table.models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ['pass_message', 'fail_message', 'created_at']
