from rest_framework import serializers
from django.contrib.auth.models import User


class UserModelSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'}, required=True)
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'}, required=True)

    class Meta:
        model = User
        fields = ['username', 'email','password', 'confirm_password']
        extra_kwargs = {
            'email': {'required': True}
            
        }

    def validate(self, data):
        """
        Check that the password and confirm_password fields match and meet certain criteria.
        """
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        
        if password != confirm_password:
            raise serializers.ValidationError("Password and confirm password do not match.")
        if len(password) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long.')
        # if not any(c.isupper() for c in password):
        #     raise serializers.ValidationError('Password must contain at least one uppercase letter.')
        return data

    def create(self, validated_data):
        """
        Create a new user with the validated data.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user





class UserLoginSerializer(serializers.Serializer): # regular serializers
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
