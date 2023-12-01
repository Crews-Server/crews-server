from rest_framework.exceptions import ParseError


class InvalidApplyException(ParseError):
    default_detail = "잘못된 지원서 작성 요청입니다."