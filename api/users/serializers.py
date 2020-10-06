import base64
import datetime
import random
import string
from django.core.cache import cache
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from urllib.parse import quote

from .models import User


def encode(text):
    enc_bytes = text.encode('ascii')
    base64_bytes = base64.b64encode(enc_bytes)
    base64_enc = base64_bytes.decode('ascii')
    return base64_enc


def decode(text):
    base64_bytes = text.encode('ascii')
    text_bytes = base64.b64decode(base64_bytes)
    decoded_text = text_bytes.decode('ascii')
    return decoded_text


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email',)

    def create(self, validated_data):
        email = validated_data['email']
        payload = email
        if (email and User.objects.filter(email=email).exists()):
            raise serializers.ValidationError(
                {'email': 'Email addresses must be unique.'}
            )
        confirmation_code = encode(
            ''.join(random.choice(
                string.ascii_uppercase + string.digits
                ) for _ in range(8))
            )
        username = email.replace('@', '_').replace('.', '_')
        email = email
        c_c = confirmation_code
        cache.set_many({'u': username, 'e': email, 'c_c': c_c}, timeout=300)
        send_mail(
            'Ваш код подтверждения',
            confirmation_code,
            'from@example.com',
            [f'{email}'],
            fail_silently=False,
        )       
        return self.data['email']


class MyAuthTokenSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('email', 'confirmation_code')

    def validate(self, data):
        send_email = self.initial_data['email']
        send_confirmation_code = data['confirmation_code']
        data = cache.get_many(['u', 'e', 'c_c'])
        if not data:
            raise serializers.ValidationError(
                'Время подтверждения регистрации истекло'
            )
        username = data['u']
        email = data['e']
        confirmation_code = data['c_c']
        if send_confirmation_code == confirmation_code:
            user = User.objects.create(
                username=username,
                email=email,
                confirmation_code=confirmation_code
            )
            user.save()
            refresh = TokenObtainPairSerializer.get_token(user)
            data['token'] = str(refresh.access_token)
            return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'username',
            'bio',
            'role'
        )
