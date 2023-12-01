from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from email.mime.text import MIMEText
import random
import smtplib

from .exceptions import NotSogangMailException, DuplicateSogangMailException
from .serializers import *
from config.settings import env
from table.models import *

User = get_user_model()

# 1 ~ 3. 회원가입 관련 api
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# 4. 서강대 이메일 중복체크 및 인증확인 메일 보내는 api
send_email = env("SEND_EMAIL")
send_pwd = env("SEND_PWD")
smtp_name = "smtp.gmail.com"
smtp_port = 587

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def sogang_mail_check(request):
    sogang_mail = request.data.get('sogang_mail')
    recv_email = sogang_mail

    if not sogang_mail.endswith('@sogang.ac.kr'):
        raise NotSogangMailException

    if not User.objects.filter(sogang_mail=sogang_mail).exists():
        raise DuplicateSogangMailException
    
    num = [random.randint(0, 9) for _ in range(6)]
    num_str = ''.join(map(str, num))

    text = f"""
        안녕하세요 서강대학교 crews입니다.
        회원 가입 인증 번호는
        {num_str} 입니다.
    """
    msg = MIMEText(text, _charset="utf-8")
    msg['Subject'] = "Crews 인증 메일"
    msg['From'] = send_email
    msg['To'] = recv_email

    s = smtplib.SMTP(smtp_name, smtp_port)
    s.starttls()
    s.login(send_email, send_pwd)
    s.sendmail(send_email, recv_email, msg.as_string())
    s.quit()

    res = {
        "message": "Mail sent successfully!",
        "verification_code" : num_str,
    }
    return Response(res, status=status.HTTP_200_OK)

# 5. 유저가 입력한 인증번호가 올바른 인증번호인지 확인하는 api
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def verification_code_check(request):
    user_input_code = request.data.get('user_input_code')  # 사용자가 메일을 확인한 뒤 입력한 코드
    verification_code = request.data.get('verification_code') # 실제 해당 사용자의 메일로 보낸 코드

    context = {}

    if user_input_code == verification_code:
        context["message"] = "Verification successful!"
        return Response(context, status=status.HTTP_200_OK)
    else:
        context["message"] = "Verification denied. Invalid code."
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
