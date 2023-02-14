from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime, timedelta
import random
from django.conf import settings
from django.utils import timezone
from .models import *
from .serializers import *
from accounts.utils import send_otp
# Create your views here.


class MyUserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer

    @action(detail=True, methods=["PATCH"])
    def verify_otp(self, request, pk=None):
        instance = self.get_object()

        if (not instance.is_active and instance.otp == request.data.get("otp") and instance.otp_expiry and timezone.now() < instance.otp_expiry):
            instance.is_active = True
            instance.otp_expiry = None
            instance.max_otp_try = settings.MAX_OTP_TRY
            instance.max_otp_out = None

            instance.save()
            return Response({"message": "Successfully verified the User."}, status=status.HTTP_200_OK)
        return Response({"message": "User is Active or Please enter the correct OTP."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["PATCH"])
    def regenerate_otp(self, request, pk=None):
        instance = self.get_object()

        if int(instance.max_otp_try) == 0 and timezone.now() < instance.max_otp_out:
            return Response({"message":"Max OTP try reached, try after an hour."}, status=status.HTTP_400_BAD_REQUEST)
        otp = random.randint(10000, 99999)
        otp_expiry = timezone.now() + timedelta(minutes=10)
        max_otp_try = int(instance.max_otp_try) - 1

        instance.otp = otp
        instance.otp_expiry = otp_expiry
        instance.max_otp_try = max_otp_try

        if max_otp_try == 0:
            instance.otp_max_out = timezone.now() + timedelta(hours=10)
        elif max_otp_try == -1:
            instance.max_otp_try = settings.MAX_OTP_TRY
        else:
            instance.otp_max_out = None
            instance.max_otp_try = max_otp_try
        print(instance.email)
        instance.save()
        # todo: send otp logic
        send_otp(instance.phone_number, otp)
        return Response({"message": "Successfully re-generated OTP"}, status=status.HTTP_200_OK)