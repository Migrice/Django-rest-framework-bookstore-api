import pyotp
from rest_framework.generics import ListCreateAPIView
from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.serializer import EmailSlr, UserCreateSlr, BaseUserSlr
from users.utils import send_account_creation_mail, send_otp_mail
from django.core.cache import cache


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

class UserSendOtpMail(ListCreateAPIView):

    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = EmailSlr

    def create(self, request, *args, **kwargs):
        serializer = EmailSlr(data=request.data)
        if serializer.is_valid():
            try:
                user= User.objects.get(email = request.data["email"])
            except User.DoesNotExist:
                raise APIException(code=status.HTTP_400_BAD_REQUEST,
                                   detail=f"User with email <<{request.data['email']}>> does not exists")

            totp = pyotp.TOTP('base32secret3232', digits=6, interval=60)
            otp_code = totp.now()
            send_otp_mail(username=user.username, email= user.email, otp=otp_code)
            print(otp_code)
            cache.set("otp_code", otp_code)
            #print("Mail send successfully")
            #code = cache.get('otp_code')
            #print("cache data", code)
            return Response( status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CheckOTPCodeValidView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        user_otp = request.data["otp_code"]
        cache_otp = cache.get('otp_code')
        if user_otp != cache_otp:
            return Response(data="Invalid OTP code", status=status.HTTP_400_BAD_REQUEST)
        return Response(data="Valid OTP", status=status.HTTP_200_OK)

