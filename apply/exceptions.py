from rest_framework.exceptions import ParseError, PermissionDenied


class InvalidApplyException(ParseError):
    default_detail = "잘못된 지원서 작성 요청입니다."

class PostAuthorException(PermissionDenied):
    default_detail = "모집 공고의 동아리 운영진이 아닙니다."