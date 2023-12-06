from rest_framework import serializers
from .models import User, FriendRequest


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Adding password field for signup

    class Meta:
        model = User
        fields = ('id', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user_email = serializers.SerializerMethodField()
    to_user_email = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at', 'from_user_email', 'to_user_email']

    def get_from_user_email(self, obj):
        return obj.from_user.email if obj.from_user else None

    def get_to_user_email(self, obj):
        return obj.to_user.email if obj.to_user else None
