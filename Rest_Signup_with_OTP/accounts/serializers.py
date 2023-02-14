from datetime import datetime, timedelta
import random
from django.conf import settings
from rest_framework import serializers
from .models import *
from accounts.utils import send_otp



class MyUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, min_length=settings.MIN_PASSWORD_LENGHT, error_messages={"min_lenght": f"Password must be longer than {settings.MIN_PASSWORD_LENGHT} characters."})
    password2 = serializers.CharField(write_only=True, min_length=settings.MIN_PASSWORD_LENGHT, error_messages={"min_lenght": f"Password must be longer than {settings.MIN_PASSWORD_LENGHT} characters."})

    class Meta:
        model = MyUser
        fields = ['phone_number', 'email', 'password1', 'password2']

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Password does not match...!")
        return data

    def create(self, validated_data):
        otp = random.randint(10000, 99999)
        otp_expiry = datetime.now() + timedelta(minutes=10)
        user = MyUser(
            phone_number=validated_data['phone_number'],
            email = validated_data['email'],
            otp = otp,
            otp_expiry = otp_expiry,
            max_otp_try = settings.MAX_OTP_TRY,
            )
        user.set_password(validated_data["password1"])
        user.save()
        # todo: send otp logic
        send_otp(validated_data['phone_number'], otp)
        return user