from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import index, ItemViewSet, RegisterViewSet, LoginViewSet, LogoutViewSet, UserProfileViewSet, register,login,logout,chat


router = DefaultRouter()
router.register('api/items', ItemViewSet, basename='items')
router.register('api/register', RegisterViewSet, basename='register')
router.register('api/login', LoginViewSet, basename='login')
router.register('api/logout', LogoutViewSet, basename='logout')
router.register('api/user', UserProfileViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('index/', index, name='index'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('chat/', chat, name='chat')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

