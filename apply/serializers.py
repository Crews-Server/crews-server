from rest_framework import serializers
from table.models import Post, Section, LongSentence, CheckBox, File, CheckBoxOption

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ['pass_message', 'fail_message', 'created_at']

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'

class LongSentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LongSentence
        fields = '__all__'

class CheckBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckBox
        fields = '__all__'

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

class CheckBoxOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckBoxOption
        fields = '__all__'