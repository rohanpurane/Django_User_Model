from rest_framework import serializers
from .models import User
from .utils import *
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type' : 'password'},write_only= True)
    class Meta:
        model = User
        fields = ['email','username','tc','password','password2']
        extra_kwargs = {
            'password' : {'write_only': True}
        }

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError('Passwords do not match...!')
        return data

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)



class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=80)
    class Meta:
        model = User
        fields = ['email','password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','username']




class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=80,style={'input_type' : 'password'},write_only= True)
    password2 = serializers.CharField(max_length=80,style={'input_type' : 'password'},write_only= True)
    class Meta:
        fields = ['password','password2']

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError('Passwords do not match...!')
        user.set_password(password)
        user.save()
        return data


class SendResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=80)
    class Meta:
        fields = ['email']

    def validate(self, data):
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            # uid = user.id
            uid = urlsafe_base64_encode(force_bytes(user.id))
            # print('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            # print('password reset token', token)
            link = 'http://localhost:3000/reset_password_link/'+uid+'/'+token+'/'
            # print('Password Reset Link', link)
            # Send Email
            data = {
                'email_subject':'Reset Your Password',
                'body':'Click on The Following Link to Reset Your Password',
                'to_email':user.email
            }
            Util.send_email(data)
            return data
        else:
            raise serializers.ValidationError('You are not Registered User')


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=80,style={'input_type' : 'password'},write_only= True)
    password2 = serializers.CharField(max_length=80,style={'input_type' : 'password'},write_only= True)
    class Meta:
        fields = ['password','password2']

    def validate(self, data):
        try:
            password = data.get('password')
            password2 = data.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError('Passwords do not match...!')
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            return data
        except DjangoUnicodeDecodeError as Identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not Valid or Expired')