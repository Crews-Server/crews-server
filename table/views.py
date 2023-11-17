from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *

from rest_framework import generics
# from rest_framework_simplejwt.views import TokenObtainPairView
# from .serializers import UserRegisterSerializer

# # 회원가입
# class UserRegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserRegisterSerializer
    
# # 로그인
# class CustomTokenObtainPairView(TokenObtainPairView):
#     pass  


###############################################
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CrewViewSet(ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer

class AdministratorViewSet(ModelViewSet):
    queryset = Administrator.objects.all()
    serializer_class = AdministratorSerializer

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostImageViewSet(ModelViewSet):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer

class ApplyViewSet(ModelViewSet):
    queryset = Apply.objects.all()
    serializer_class = ApplySerializer

class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

class SectionViewSet(ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

class LongSentenceViewSet(ModelViewSet):
    queryset = LongSentence.objects.all()
    serializer_class = LongSentenceSerializer

class LongSentenceAnswerViewSet(ModelViewSet):
    queryset = LongSentenceAnswer.objects.all()
    serializer_class = LongSentenceAnswerSerializer

class CheckBoxViewSet(ModelViewSet):
    queryset = CheckBox.objects.all()
    serializer_class = CheckBoxSerializer

class CheckBoxOptionViewSet(ModelViewSet):
    queryset = CheckBoxOption.objects.all()
    serializer_class = CheckBoxOptionSerializer

class CheckBoxAnswerViewSet(ModelViewSet):
    queryset = CheckBoxAnswer.objects.all()
    serializer_class = CheckBoxAnswerSerializer

class FileViewSet(ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

class FileAnswerViewSet(ModelViewSet):
    queryset = FileAnswer.objects.all()
    serializer_class = FileAnswerSerializer

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class ScoreViewSet(ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer