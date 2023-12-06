from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework import generics

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from .models import User, FriendRequest
from .serializers import (UserSerializer, UserLoginSerializer, 
                          FriendRequestSerializer,)
from .utils import FriendRequestThrottle


class UserSignupAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate(request, email=email, password=password)
        
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 
                             'msg': 'Login successful'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'token': "", 
                             'msg': 'Invalid credentials'}, 
                            status=status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUserAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserSearchAPIView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        search_param = self.request.query_params.get('search')
        
        if search_param:
            # Check if the search_param matches an exact email
            if '@' in search_param:
                return User.objects.filter(email__iexact=search_param)
            
            # Search by name if keyword is part of name
            return User.objects.filter(Q(name__icontains=search_param))
        return User.objects.none()  
    

class SendFriendRequestAPIView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerializer
    throttle_classes = [FriendRequestThrottle]

    def post(self, request, *args, **kwargs):
        from_user = request.user
        to_user_id = request.data.get('to_user_id')

        if not to_user_id:
            return Response({'error': 'to_user_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            to_user = User.objects.get(id=to_user_id)

            if from_user == to_user:
                return Response({'error': 'from_user and to_user cannot be the same.'}, 
                                status=status.HTTP_400_BAD_REQUEST)
            
            # Check if friend request already exists between from_user and to_user
            existing_request = FriendRequest.objects.filter(
                (Q(from_user=from_user, to_user=to_user) | Q(from_user=to_user, to_user=from_user)),
                ~Q(status='rejected')
            )

            if existing_request.exists():
                if existing_request.filter(to_user=from_user):
                    return Response({'error': 'Friend request already present. Confirm Request.'}, 
                                    status=status.HTTP_400_BAD_REQUEST)

                return Response({'error': 'Friend request already sent.'}, 
                                status=status.HTTP_400_BAD_REQUEST)

            FriendRequest.objects.create(from_user=from_user, to_user=to_user)
            return Response({'message': 'Friend request sent successfully.'}, 
                            status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response({'error': 'Invalid to_user_id.'}, status=status.HTTP_404_NOT_FOUND)


class AcceptRejectFriendRequestAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        current_user = request.user
        request_id = request.data.get('request_id')
        action = request.data.get('action')

        # allow only 'accept' and 'reject' actions
        allowed_action = ['accept', 'reject']

        if not request_id or not action or action not in allowed_action:
            return Response(
                {'error': 'request_id and action are required & allowed actions: accept, reject'}, 
                status=status.HTTP_400_BAD_REQUEST)

        try:
            friend_request = FriendRequest.objects.get(
                id=request_id, to_user=current_user, status='pending')

            if action == 'accept':
                friend_request.status = 'accepted'
                friend_request.save()
                return Response({'message': 'Friend request accepted.'})
                
            elif action == 'reject':
                friend_request.status = 'rejected'
                friend_request.save()
                return Response({'message': 'Friend request rejected.'})

        except FriendRequest.DoesNotExist:
            return Response(
                {'error': 'Friend request not found or already processed.'}, 
                status=status.HTTP_404_NOT_FOUND)


class ListFriendsAPIView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        current_user_id = user.id

        friends = FriendRequest.objects.filter(
            Q(from_user=user) |  # Sender is the user OR
            Q(to_user=user),   # Recipient is the user
            status='accepted'  # Friend request is accepted
        )

        friend_ids = list(friends.values_list('from_user_id', flat=True)) + \
             list(friends.values_list('to_user_id', flat=True))

        friend_ids = list(set(friend_ids))

        if current_user_id in friend_ids:
            friend_ids.remove(current_user_id)
        
        # Fetch user profiles of friends
        return User.objects.filter(id__in=friend_ids)
    

class ListPendingFriendRequestsAPIView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        user = self.request.user
        # Fetch pending friend requests received by the authenticated user
        return FriendRequest.objects.filter(to_user=user, status='pending')
