from django.urls import path
from django.contrib import admin
from social_app.views import (
    UserRegistrationView,
    UserLoginView,
    UserSearchView,
    FriendRequestView,
    FriendRequestResponseView,
    FriendsListView,
    PendingFriendRequestsView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='user_search'),
    path('friend-request/', FriendRequestView.as_view(), name='friend_request'),
    path('friend-request-response/<int:pk>/', FriendRequestResponseView.as_view(), name='friend_request_response'),
    path('friends/', FriendsListView.as_view(), name='friends_list'),
    path('pending-requests/', PendingFriendRequestsView.as_view(), name='pending_requests'),
]
