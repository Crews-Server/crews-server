from rest_framework import serializers

from .models import LongSentence, CheckBox, File, CheckBoxOption, Apply, LongSentenceAnswer, CheckBoxAnswer, FileAnswer
from post.models import Section

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

class ApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Apply
        fields = '__all__'

class LongSentenceAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LongSentenceAnswer
        fields = '__all__'

class CheckBoxAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckBoxAnswer
        fields = '__all__'

class FileAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileAnswer
        fields = '__all__'