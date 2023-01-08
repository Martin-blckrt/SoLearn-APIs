from rest_framework import serializers
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(email=self.validated_data['email'])
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"}, required=True)
    new_password = serializers.CharField(style={"input_type": "password"}, required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError({'current_password': 'Does not match'})
        return value
        

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(style={"input_type": "email"}, required=True)
    password = serializers.CharField(style={"input_type": "password"}, required=True)
    

class ConfirmSerializer(serializers.Serializer):
    token = serializers.CharField(style={"input_type": "token"}, required=True)
    

class CheckTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(style={"input_type": "access_token"}, required=True)