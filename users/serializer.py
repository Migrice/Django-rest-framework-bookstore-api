from rest_framework import serializers

from users.models import User

class BaseUserSlr(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','username','email']

class UserCreateSlr(serializers.ModelSerializer):
    password2 = serializers.CharField(required=True,allow_blank=False)


    class Meta:
        model = User
        fields = ['id','username','email','password','password2']

        extra_kwargs={
            'id':{'read_only':True},
            'password':{'write_only':True},
            'password2':{'write_only':True}
        }

    def save(self, request):
        try:
            #connected_user= request.user
            v_user = self.validated_data
            print(self.validated_data)

            user = User(
                #createdby=connected_user,
                #editedby=connected_user,
                username=v_user.get('username', None),
                email=v_user.get('email',None)

            )
            user.set_password(v_user['password'])
            user.save()
            return user
        except Exception as e:
            print('Can not create the user')
            print("Exeption",e)

class EmailSlr(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_blank=False)

    class Meta:
        model = User
        fields = ["email"]
