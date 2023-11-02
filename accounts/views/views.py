from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from accounts.serializers.user_serializer import UserSerializer
from ..models import User
from ..serializers import UserLoginSerializer


# Create your views here.

@api_view(["POST"])
@csrf_exempt
def user_register(request) -> JsonResponse:

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def user_login(request) -> JsonResponse:

    serializer = UserLoginSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.validated_data
        # La Función que verdaderamente hace el login
        login(request, user)
        user_serializer = UserSerializer(user)
        return JsonResponse(user_serializer.data, status=status.HTTP_200_OK)

    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_test(request) -> JsonResponse:
    users = User.objects.all()
    users = UserSerializer(users, many=True)
    return JsonResponse(users.data, safe=False, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_logout(request):
    logout(request)
    return JsonResponse(
        data={"message": "User logged out successfully"},
        status=status.HTTP_200_OK
    )