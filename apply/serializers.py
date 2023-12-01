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
    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        return "long_sentence"
    
    class Meta:
        model = LongSentence
        fields = ('question', 'letter_count_limit', 'is_essential', 'sequence', 'section', 'type')

class CheckBoxSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        return "checkbox"
    
    class Meta:
        model = CheckBox
        fields = ('question', 'is_essential', 'answer_minumum', 'answer_maximum', 'sequence', 'section', 'type')

class FileSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        return "file"
    
    class Meta:
        model = File
        fields = ('question', 'is_essential', 'sequence', 'section', 'type')

class CheckBoxOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckBoxOption
        fields = '__all__'