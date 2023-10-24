from rest_framework_simplejwt.views import TokenObtainPairView

from users.jwt_slr import MyTokenObtainPairSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
