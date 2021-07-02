from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from .models import Follow, Group, Post, User
from .permissions import IsOwnerOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)

AUTHENTICATED_OR_READ_ONLY = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
AUTHENTICATED = (IsAuthenticated, IsOwnerOrReadOnly)


class CreateListGenericViewSet(mixins.CreateModelMixin, 
                                mixins.ListModelMixin,
                                viewsets.GenericViewSet):
    pass


@permission_classes(AUTHENTICATED_OR_READ_ONLY)
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group', ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@permission_classes(AUTHENTICATED_OR_READ_ONLY)
class GroupViewSet(CreateListGenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


@permission_classes(AUTHENTICATED)
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return post.comments  

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


@permission_classes(AUTHENTICATED)
class FollowViewSet(CreateListGenericViewSet):
    serializer_class = FollowSerializer
    filter_backends = [filters.SearchFilter]
    filterset_fields = ['following', ]
    search_fields = ['user__username', 'following__username']

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return Follow.objects.filter(following=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
