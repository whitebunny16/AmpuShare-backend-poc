from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from .models import Profile, Buddy
from .serializers import UserLoginSerializer, ProfileSerializer, UserRegistrationSerializer, PasswordResetSerializer, \
    PasswordResetConfirmSerializer, BuddySerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    """
    User login
    :param request:
    :return:
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        access = AccessToken.for_user(user)

        response_data = {
            'access': str(access),
            'refresh': str(refresh),
            'user': {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'profile_image': user.profile.profile_pic.url if hasattr(user,
                                                                         'profile') and user.profile.profile_pic else None
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_register(request):
    """
    User register
    :param request:
    :return:
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset(request):
    """
    Password reset
    :param request:
    :return:
    """
    serializer = PasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        # Django Mail + pyOTP
        return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request):
    """
    Password reset
    :param request:
    :return:
    """
    serializer = PasswordResetConfirmSerializer(data=request.data)
    if serializer.is_valid():
        return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_profile(request, username):
    """
    User profile
    :param request:
    :param username:
    :return:
    """
    usr_profile = get_object_or_404(Profile, user__username=username)
    serializer = ProfileSerializer(usr_profile)
    return Response(serializer.data)


@api_view(['GET', 'PUT'])
def own_profile(request):
    """
    Own profile
    :param request:
    :return:
    """
    usr_profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'GET':
        serializer = ProfileSerializer(usr_profile)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProfileSerializer(usr_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def follow_user(request, user_id):
    """
    Follow user
    :param request:
    :param user_id:
    :return:
    """
    follow_data = {'follower': request.user.id, 'following': user_id}
    serializer = BuddySerializer(data=follow_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def unfollow_user(request, user_id):
    """
    Unfollow user
    :param request:
    :param user_id:
    :return:
    """
    follow_instance = get_object_or_404(Buddy, follower=request.user.id, following=user_id)
    follow_instance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def followers_list(request, user_id):
    """
    Followers list
    :param request:
    :param user_id:
    :return:
    """
    followers = Buddy.objects.filter(following=user_id)
    serializer = BuddySerializer(followers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def following_list(request, user_id):
    """
    Followers list
    :param request:
    :param user_id:
    :return:
    """
    following = Buddy.objects.filter(follower=user_id)
    serializer = BuddySerializer(following, many=True)
    return Response(serializer.data)
