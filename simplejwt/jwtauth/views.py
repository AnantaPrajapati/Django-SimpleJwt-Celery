from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from .serializers import UserSeriazlier, VerifySerializer, NoticeSerializer, LoginSerializer
from rest_framework.response import Response
from .models import UserData
from rest_framework.decorators import action
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Notice
from .customauthentication import IsAuthenticatedWithJWT
from .tasks import reverse
from rest_framework.decorators import api_view
from .tasks import send_mail_all
# from simplejwt.celery import add
# from .tasks import send_email

@api_view(['POST'])
def send_email(request):
     send_mail_all.delay()
     return HttpResponse("Email sent successfully")

@api_view(['GET'])
def test(request):
     reverse.delay("hello")
     return HttpResponse("Done")

class RegisterUserViewset(viewsets.ModelViewSet):
       queryset = UserData.objects.all()
       serializer_class = UserSeriazlier
       permission_classes = [permissions.AllowAny]
       authentication_classes = []


       
     # @action(methods=['post'], detail = False, permission_classes =[permissions.AllowAny])
       def create(self, request):
            serializer = self.get_serializer(data = request.data)
            serializer.is_valid(raise_exception= True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({
            "message": "User registered successfully. An OTP has been sent to your email.",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)
       
       @action(detail = False, methods = ['post'], permission_classes = [permissions.AllowAny])
       def verify_otp(self, request):
            serializer = VerifySerializer(data = request.data)
            serializer.is_valid(raise_exception=True)

            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']

            try:
                 user = UserData.objects.get(email= email)
            except UserData.DoesNotExist:
                 return Response({'error': 'user not found'}, status = status.HTTP_400_BAD_REQUEST)
            
            if user.otp == otp:
                 user.is_verified = True
                 user.otp = None
                 user.save()
                 send_mail(
                 'Email Verification OTP',
                 f'Your OTP for email verification is : {otp}',
                 settings.EMAIL_HOST_USER,
                 [email],
                 fail_silently = False
                 )
                 
                 return Response({"success":"User is verified successfully"}, status = status.HTTP_200_OK)
            else:
                 return Response({"error":"Invalid Otp"}, status = status.HTTP_400_BAD_REQUEST)


class LoginViewSet(viewsets.ModelViewSet):
    queryset = UserData.objects.all()
    serializer_class = LoginSerializer 
    http_method_names = ['post']
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email = email, password= password)
        
        if user is None:
             return Response({'error':'User is not found'}, status = status.HTTP_400_BAD_REQUEST)
        
        if not user.is_verified:
             return Response({'error':'User is not verified'}, status = status.HTTP_400_BAD_REQUEST)
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = Response({"message":"Login successful"}, status = status.HTTP_200_OK)
        response.set_cookie(
             key = 'jwt',
             value = access_token,
             httponly= True,
             secure=True,
             samesite= 'Lax',
        )
        response.set_cookie(
             key='refresh',
             value=str(refresh),
             httponly= True,
             secure= True,
             samesite='lax',
        )
        return response


class AddNotice(viewsets.ModelViewSet):
     queryset = Notice.objects.all()
     serializer_class = NoticeSerializer
     http_method_names  = ['post']
     authentication_classes = [IsAuthenticatedWithJWT]
     permission_classes = [permissions.IsAuthenticated] 


     def create(list, request):
          serializer = NoticeSerializer(data = request.data)
          serializer.is_valid(raise_exception = True)

          # title = serializer.validated_data['title']
          # description = serializer.validated_data['description']
          # image = serializer.validated_data['image']

          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data, status =status.HTTP_200_OK)
          else:
               return Response(serializer.error_messages, status = status.HTTP_400_BAD_REQUEST)


class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    http_method_names = ['get']
    authentication_classes = [IsAuthenticatedWithJWT]
    permission_classes = [permissions.IsAuthenticated] 

    def list(self, request):
        notices = self.get_queryset()
     #    result = add.delay(10, 20)
     #    print("result :", result)
        serializer = NoticeSerializer(notices, many = True)
        return Response({"notices":serializer.data}, status = status.HTTP_200_OK)
    

class LogoutViewSet(viewsets.ModelViewSet):
     authentication_classes = []  # Ensure no authentication is required
     permission_classes = [permissions.AllowAny]
     @action(detail=False, methods=['post'])
     def logout(self, request):
          response = Response({"message":"Logged out successfully"}, status = status.HTTP_200_OK)
          response.delete_cookie('jwt')
          response.delete_cookie('refresh')
          return response
  