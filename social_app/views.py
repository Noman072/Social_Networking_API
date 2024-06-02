
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import (   
    UserLoginSerializer, 
    UserProfileSerializer, 
    UserRegistrationSerializer,
    FriendRequestSerializer
)
from django.contrib.auth import authenticate
from .renderers import uSerRenderers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User, FriendRequest
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from django.core.cache import cache
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token': token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email').lower()
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

#Logged in user profile
class UserProfileView(APIView):
    renderer_classes = [uSerRenderers]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

#Pagination for Searching other users
class UserSearchPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

#searching other users
class UserSearchView(generics.ListAPIView):
    renderer_classes = [uSerRenderers]
    serializer_class = UserProfileSerializer
    pagination_class = UserSearchPagination

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        if '@' in query:
            return User.objects.filter(email__iexact=query)
        else:
            return User.objects.filter(Q(name__icontains=query) | Q(email__icontains=query))

#Sending friend request
class FriendRequestView(APIView):
    renderer_classes = [uSerRenderers]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        if not request.user.is_authenticated:
            return Response({'errors': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        to_user_id = request.data.get('to_user_id')
        to_user = User.objects.get(id=to_user_id)

        # Check rate limit
        user_id = request.user.id
        friend_requests_count = cache.get(f'friend_requests_count_{user_id}', 0)
        if friend_requests_count >= 3:
            return Response({'errors': 'You have reached the limit of 3 friend requests per minute'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        # Create friend request
        friend_request, created = FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
        if not created:
            return Response({'errors': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)

        # Update rate limit cache
        cache.set(f'friend_requests_count_{user_id}', friend_requests_count + 1, timeout=60)

        return Response({'msg': 'Friend request sent'}, status=status.HTTP_201_CREATED)

#Responding to pending friend request
class FriendRequestResponseView(APIView):
    renderer_classes = [uSerRenderers]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        status_choice = request.data.get('status')
        friend_request = FriendRequest.objects.get(id=pk, to_user=request.user)
        if status_choice not in ['accepted', 'rejected']:
            return Response({'errors': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        friend_request.status = status_choice
        friend_request.save()
        return Response({'msg': f'Friend request {status_choice}'}, status=status.HTTP_200_OK)

#See friend lists
class FriendsListView(APIView):
    renderer_classes = [uSerRenderers]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        friends = User.objects.filter(sent_friend_requests__status='accepted', sent_friend_requests__to_user=request.user)
        serializer = UserProfileSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#See pending friend lists
class PendingFriendRequestsView(APIView):
    renderer_classes = [uSerRenderers]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        pending_requests = FriendRequest.objects.filter(to_user=request.user, status='pending')
        serializer = FriendRequestSerializer(pending_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
