from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.http import JsonResponse
from .models import Item, ItemUser
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password, check_password
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

class RegisterViewSet(viewsets.ViewSet):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def create(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(viewsets.ViewSet):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def create(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        user_data = {
            'name': user.name,
            'email': user.email,
            'mobile': user.mobile,
        }
        return Response(user_data)

        
class ItemViewSet(viewsets.ViewSet):
    parser_classes = (MultiPartParser, FormParser)

    def list(self, request):
        items = Item.objects.all()
        items_list = []
        for item in items:
            items_list.append({
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'image': request.build_absolute_uri(item.image.url) if item.image else ''
            })
        return JsonResponse(items_list, safe=False)

    def create(self, request):
        try:
            data = request.data
            item = Item.objects.create(
                name=data['name'],
                description=data['description'],
                image=data.get('image')
            )
            return JsonResponse({
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'image': request.build_absolute_uri(item.image.url) if item.image else ''
            }, status=status.HTTP_201_CREATED)
        except KeyError:
            return JsonResponse({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            item = Item.objects.get(pk=pk)
            item_data = {
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'image': request.build_absolute_uri(item.image.url) if item.image else ''
            }
            return JsonResponse(item_data)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            item = Item.objects.get(pk=pk)
            data = request.data
            item.name = data['name']
            item.description = data['description']
            if 'image' in data:
                item.image = data['image']
            item.save()
            return JsonResponse({
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'image': request.build_absolute_uri(item.image.url) if item.image else ''
            })
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return JsonResponse({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            item = Item.objects.get(pk=pk)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

def index(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'signup.html')

def login(request):
    return render(request, 'login.html')

def logout(request):
    logout(request)
    return redirect('/login/')

def chat(request):
    return render(request, 'chat.html')