from rest_framework import status
from rest_framework.exceptions import ParseError, APIException

class NotSogangMailException(ParseError):
    default_detail = "서강대학교 이메일이 아닙니다."

class DuplicateSogangMailException(APIException):
    default_detail = "이미 가입된 서강대학교 이메일입니다."
    status_code = status.HTTP_403_FORBIDDEN