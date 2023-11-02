from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from accounts.serializers.user_serializer import UserSerializer
from ..models import User
from ..serializers import UserLoginSerializer


# Create your views here.

@api_view(["POST"])
@csrf_exempt
def user_register(request):

    serializer = UserSerializer(data=request.POST)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def user_login(request):

    serializer = UserLoginSerializer(data=request.POST)

    if serializer.is_valid():
        user = serializer.validated_data
        # La Función que verdaderamente hace el login
        login(request, user)
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_test(request):
    users = User.objects.all()
    users = UserSerializer(users, many=True)
    return Response(users.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def user_logout(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)