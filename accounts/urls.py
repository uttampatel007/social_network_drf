from django.urls import path
from .views import (UserSignupAPIView, UserLoginAPIView, AuthenticatedUserAPIView,
                    UserSearchAPIView, SendFriendRequestAPIView, AcceptRejectFriendRequestAPIView,
                    ListFriendsAPIView,
                    ListPendingFriendRequestsAPIView)


urlpatterns = [
    path('signup/', UserSignupAPIView.as_view(), name='user_signup'),
    path('login/', UserLoginAPIView.as_view(), name='user_login'),
    path('user/', AuthenticatedUserAPIView.as_view(), name='authenticated_user'),
    path('search/', UserSearchAPIView.as_view(), name='user-search'),
    path('send-friend-request/', SendFriendRequestAPIView.as_view(), name='send-friend-request'),
    path('update-friend-request/', AcceptRejectFriendRequestAPIView.as_view(), name='accept-reject-friend-request'),
    path('friends/', ListFriendsAPIView.as_view(), name='list-friends'),
    path('pending-requests/', ListPendingFriendRequestsAPIView.as_view(), name='list-pending-friend-requests'),
]
