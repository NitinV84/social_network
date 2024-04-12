from rest_framework import serializers
from .models import FriendRequest


class FriendRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for creating friend requests
    """
    class Meta:
        model = FriendRequest
        fields = ['request_to']

    def create(self, validated_data):
        request_from = self.context.get('request_from')
        request_to = validated_data.get('request_to')

        # Check if user has already sent the request
        friend_request = FriendRequest.objects.filter(
            request_from=request_from,
            request_to=request_to,
            status__in=['accepted', 'pending']
        ).first()

        if not friend_request:
            return FriendRequest.objects.create(
                request_from=request_from,
                request_to=request_to,
                status='pending'
            )
        return friend_request
    

class FriendRequestSerializerGET(serializers.ModelSerializer):
    """
    Serializer for getting pending requests
    """
    class Meta:
        model = FriendRequest
        fields = ['id']


class FriendRequestUpdateSerializer(serializers.ModelSerializer):
    """ 
    Serializer for accepting and rejecting friend requests 
    """
    STATUS_CHOICES = [
        ('accepted', 'accepted'),
        ('rejected', 'rejected'),
    ]

    status = serializers.ChoiceField(choices=STATUS_CHOICES)
    id = serializers.PrimaryKeyRelatedField(queryset=FriendRequest.objects.all())

    class Meta:
        model = FriendRequest
        fields = ['status', 'id']

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status')
        instance.save()

        if instance.status == 'accepted':
            instance.request_to.friends.add(instance.request_from)
        
        return instance
