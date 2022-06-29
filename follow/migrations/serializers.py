# from django.shortcuts import get_object_or_404
#
# from rest_framework import serializers
#
# from .models import Follow
#
#
# class UserFollowerListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Follow
#         exclude = ["follow_at","id", "followed"]
#
#
# class UserFollowingListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Follow
#         exclude = ["follow_at" "id", "follower"]
#
#
# class FollowSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Follow
#         exclude = ["follow_at", "id"]
#
#     def create(self, validated_data):
#         follower = self.context["follower"]
#         followed = validated_data["followed"]
#         return Follow.objects.create(follower=follower, followed=followed)
