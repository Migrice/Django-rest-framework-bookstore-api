from django.urls import path

from .views import ListCreateUserView

urlpatterns=[
    path('', ListCreateUserView.as_view(), name='list-create-user')
]
