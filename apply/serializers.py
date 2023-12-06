from rest_framework import serializers

from table.models import Post, PostImage, Section, LongSentence, CheckBox, File, CheckBoxOption, Apply, LongSentenceAnswer, CheckBoxAnswer, FileAnswer


class PostImageSerializer(serializers.ModelSerializer):
    post_image = serializers.ImageField(use_url=True)

    class Meta:
        model = PostImage
        fields = ['post_image']

class PostSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    def get_images(self, obj):
        image = obj.post_image.all() 
        return PostImageSerializer(instance=image, many=True, context=self.context).data

    def get_thumbnail(self, obj):
        thumbnail = obj.post_image.filter(is_thumbnail=True).first()
        return PostImageSerializer(instance=thumbnail, context=self.context).data

    class Meta:
        model = Post
        exclude = ['pass_message', 'fail_message', 'created_at']

    def create(self, validated_data):
        instance = Post.objects.create(**validated_data)
        image_set = self.context['request'].FILES

        thumbnail_image = image_set.get('thumbnail')

        if thumbnail_image:
            PostImage.objects.create(post=instance, post_image=thumbnail_image, is_thumbnail=True)

        for image_data in image_set.getlist('image'):
            PostImage.objects.create(post=instance, post_image=image_data, is_thumbnail=False)
        return instance

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