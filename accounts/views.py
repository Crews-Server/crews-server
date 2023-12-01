from table.models import *
from .serializers import *

from django.contrib.auth import get_user_model

from rest_framework import generics, permissions, status

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

# 여기 아래 두 줄에 노란색 밑줄 떠도 걱정 ㄴㄴ -> 잘 작동 됨.
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from django.utils import timezone  # now = timezone.now() 이렇게 사용하기

import random, os


User = get_user_model()

# 1 ~ 3. 회원가입 관련 api
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# 4. 서강대 이메일 중복체크 및 인증확인 메일 보내는 api
import smtplib
from email.mime.text import MIMEText
# from config.settings import get_env
from config.settings import env

# send_email = get_env("SEND_EMAIL")
# send_pwd = get_env("SEND_PWD")
send_email = env("SEND_EMAIL")
send_pwd = env("SEND_PWD")
smtp_name = "smtp.gmail.com"
smtp_port = 587

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def sogang_mail_check(request):
    # post-man 테스트 완료!

    sogang_mail = request.data.get('sogang_mail')  # 서강 이메일 클라이언트로부터 body로 받아오기!
    recv_email = sogang_mail

    # @sogang.ac.kr로 끝나는지 체크
    if not sogang_mail.endswith('@sogang.ac.kr'):
        context = {
            "message": "Please provide a valid Sogang University email!",
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)


    # sogang_mail 중복 체크
    try:
        user = User.objects.get(sogang_mail = sogang_mail)
    except User.DoesNotExist:
        # 만약 해당 sogang_mail로 가입한 계정이 없다면(정상적인 경우라면)

        # 난수로 6자리 정수 만들기
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
        print(msg.as_string())

        s = smtplib.SMTP(smtp_name, smtp_port)
        s.starttls()
        s.login(send_email, send_pwd)
        s.sendmail(send_email, recv_email, msg.as_string())
        s.quit()

        context = {
            "message": "Mail sent successfully!",
            "verification_code" : num_str,
        }
        return Response(context, status=status.HTTP_200_OK)
        

    # 이미 해당 sogang_mail로 회원가입을 한 상황이라면 
    context = {
        "message": "This Sogang Mail already exists!!",
    }
    return Response(context, status=status.HTTP_403_FORBIDDEN)


# 5. 유저가 입력한 인증번호가 올바른 인증번호인지 확인하는 api
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def verification_code_check(request):
    # post-man 테스트 완료!

    user_input_code = request.data.get('user_input_code')  # 사용자가 메일을 확인한 뒤 입력한 코드
    verification_code = request.data.get('verification_code') # 실제 해당 사용자의 메일로 보낸 코드

    context = {}

    if user_input_code == verification_code:
        context["message"] = "Verification successful!"
        return Response(context, status=status.HTTP_200_OK)
    else:
        context["message"] = "Verification denied. Invalid code."
        return Response(context, status=status.HTTP_400_BAD_REQUEST)


    