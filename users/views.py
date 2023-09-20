from rest_framework.generics import ListCreateAPIView
from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from django.core.mail import send_mail

from users.models import User
from users.serializer import UserCreateSlr, BaseUserSlr
from users.utils import send_account_creation_mail




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
            usr_email = User.objects.filter(username = request.data["email"])
            if usr_email:
                raise APIException(code=status.HTTP_409_CONFLICT,
                                   detail="There is another user with this email")
            created_user = serializer.save(request)

            serializer = BaseUserSlr(created_user)

            try:
                send_account_creation_mail(request.data["username"],
                                           request.data["email"])

                # message = f"""
                # <p>Hello {request.data["username"]},
                # <br/>
                # Your account has been created succesfully.

                # """

                # send_mail(subject= "Account creation",
                #           message=message,
                #           from_email="efomenakuete@gmail.com",
                #           recipient_list=[request.data["email"]])
                return Response(status=status.HTTP_200_OK,
                                data={'data':"Mail send successfully"})
            except Exception as e:
                print("error",e)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise APIException(code=status.HTTP_400_BAD_REQUEST,
                           detail=serializer.errors)


    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserCreateSlr
        else:
            return BaseUserSlr
