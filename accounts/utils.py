from rest_framework.throttling import UserRateThrottle


class FriendRequestThrottle(UserRateThrottle):
    scope = 'friend_request'

    def get_cache_key(self, request, view):
        user = request.user
        if user.is_authenticated:
            return f'{self.scope}_{user.id}'
        else:
            return f'{self.scope}_{self.get_ident(request)}'
        
