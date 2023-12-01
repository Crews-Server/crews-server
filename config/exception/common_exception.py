from rest_framework.exceptions import NotFound


class NotFountExeption(NotFound):
    postfix = " is not found."

    def __init__(self, obj):
        super().__init__(detail=obj+self.postfix)
