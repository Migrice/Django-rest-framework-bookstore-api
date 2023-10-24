from django.urls import path

from .views import CheckOTPCodeValidView, ListCreateUserView, UserSendOtpMail

urlpatterns=[
    path('', ListCreateUserView.as_view(), name='list-create-user'),
    path('send_otp_mail/', UserSendOtpMail.as_view(), name='send_otp_mail'),
    path('verify_otp/', CheckOTPCodeValidView.as_view(), name='verify-otp')

]
