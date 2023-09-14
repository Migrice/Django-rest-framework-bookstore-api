from rest_framework.generics import ListCreateAPIView
from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from users.models import User
from users.serializer import UserCreateSlr, BaseUserSlr

class ListCreateUserView(ListCreateAPIView):
    queryset=User.objects.all()
    serializer_class=BaseUserSlr


    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if request.data["password"] != request.data["password2"]:
                raise APIException(code=status.HTTP_400_BAD_REQUEST,
                                   detail="The two password must match")
            usr = User.objects.filter(username = request.data["username"])
            if usr:
                raise APIException(code=status.HTTP_409_CONFLICT,
                                   detail="There is another user with this username")
            created_user = serializer.save(request)

            serializer = BaseUserSlr(created_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise APIException(code=status.HTTP_400_BAD_REQUEST,
                           detail=serializer.errors)


    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserCreateSlr
        else:
            return BaseUserSlr
