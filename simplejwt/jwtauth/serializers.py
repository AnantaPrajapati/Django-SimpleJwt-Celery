from rest_framework import serializers
from .models import UserData, Notice, NoticeImage
from .auth import generate_otp
from django.core.mail import send_mail
from django.conf import settings
from .tasks import send_mail_one
# from .tasks import send_Email

class UserSeriazlier(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ["id", "email", "name", "password", "otp", "is_verified"]
        extra_kwargs = {
             'password':{'write_only': True},
             'otp': {'read_only': True},
             'is_verified': {'read_only': True}
         }
        
    def create(self, validated_data):
        user = UserData.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        send_mail_one.delay(user.id)
        # otp = generate_otp()
        # user.otp = otp
        # user.save()
        # send_mail(
        #     'Email Verification OTP',
        #     f'Your OTP for email verification is : {otp}',
        #     settings.EMAIL_HOST_USER,
        #     [validated_data['email']],
        #     fail_silently = False
        # )
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        model = UserData
        fields = ['email', 'password']
    
class VerifySerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

    class Meta:
        model = UserData
        fields = ['email', 'otp']


class NoticeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeImage
        fields = ['id', 'notice', 'image']


class NoticeSerializer(serializers.ModelSerializer):
    images = NoticeImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=100000, allow_empty_file=False, use_url=False),
        write_only=True
    )

    class Meta:
        model = Notice
        fields = ['id', 'title', 'description', 'images', 'uploaded_images']

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        notice = Notice.objects.create(**validated_data)

        for image in uploaded_images:
            NoticeImage.objects.create(notice=notice, image=image)

        return notice
