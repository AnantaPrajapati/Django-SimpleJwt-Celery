from django.urls import path, include
from rest_framework.routers import DefaultRouter
from jwtauth import views

router = DefaultRouter()
router.register(r'register', views.RegisterUserViewset, basename='register')
router.register(r'login', views.LoginViewSet, basename='login')
router.register(r'logout', views.LogoutViewSet, basename = 'logout')
router.register(r'View', views.NoticeViewSet, basename='view')
router.register(r'add', views.AddNotice, basename='add')

urlpatterns = [
    # path('login/', views.CustomUserViewSet, name='register'),
    path('', include(router.urls)),
    path('test/', views.test, name = 'test'),
    path('sendmail/', views.send_email, name ='sendmail')
]