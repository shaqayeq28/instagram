from django.shortcuts import  get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import authentication, permissions
from rest_framework.decorators import action

from .migrations.serializers import FollowSerializer, UserFollowerListSerializer, UserFollowingListSerializer
from .models import Follow


class Profile(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        qs_followers = Follow.objects.filter(followed__id=pk, status="a").count()
        qs_following = Follow.objects.filter(follower__id=pk, status="a").count()
        return JsonResponse({"following": qs_following, "followers": qs_followers}, safe=False)

    def post(self, request, pk=None):
        qs = get_object_or_404(User, pk=pk)
        serializer = FollowSerializer(data=request.data, context={"follower": request.user, "followed": qs})
        if qs == request.user:
            return Response(status=403)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(serializer.errors)

class FollowerCRUD(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def list(self, request):
        qs = Follow.objects.filter(followed=request.user, status="a")
        serializer = UserFollowerListSerializer(qs, many=True)
        return Response(serializer.data)


    @action(methods=["GET"], detail=False, url_path="user-following-list")
    def user_following_list(self, request):
        qs = Follow.objects.filter(follower=request.user, status="a")
        serializer = UserFollowingListSerializer(qs, many=True)
        return Response(serializer.data)

    @action(methods=["POST"], detail=False, url_path="follow-request/<int:pk>")
    def follow_request(self, request, pk):
        qs = settings.AUTH_USER_MODEL.get(user__pk=pk)
        serializer = FollowSerializer(data=request.data, context={"follower": request.user, "followed": qs})
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(serializer.errors)

    @action(methods=["GET"], detail=False, url_path="pending-list")
    def pending_list(self, request):
        qs = Follow.objects.filter(follower=request.user, status="p")
        serializer = UserFollowingListSerializer(qs, many=True)
        return Response(serializer.data)

    @action(methods=["POST"], detail=True, url_path="accept-request")
    def accept_request(self, request, pk=None):
        user_follower = get_object_or_404(User, pk=pk)
        qs = get_object_or_404(Follow, follower=user_follower, followed=request.user)
        if user_follower == request.user:
            return Response(status=403)
        qs.status = "a"
        qs.save()
        return Response(status=200)

    @action(methods=["POST"], detail=True, url_path="reject-unfollow")
    def reject_unfollow(self, request, pk=None):
        user_follower = get_object_or_404(User, pk=pk)
        qs = get_object_or_404(Follow, follower=user_follower, followed=request.user)
        if user_follower == request.user:
            return Response(status=403)
        qs.delete()
        return Response(status=204)
