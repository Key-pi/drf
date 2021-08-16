from blog.models import Blog, Comment

from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from . import serializers
from .pagination import PostLimitOffsetPagination
from .premissions import IsOwnerOrReadOnly


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    pagination_class = PostLimitOffsetPagination
    permission_classes = [IsAuthenticated]


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = serializers.BlogSerializer
    pagination_class = PostLimitOffsetPagination
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    pagination_class = PostLimitOffsetPagination
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


