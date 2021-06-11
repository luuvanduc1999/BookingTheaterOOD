from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, DestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import ValidationError

from system.serializers import PostSerializer, UserSerializer

class PostPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

class PostList(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id',)
    search_fields = ('title',)
    pagination_class = PostPagination

    def get_queryset(self):
        return super().get_queryset()

class PostCreate(CreateAPIView):
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        try:
            title = request.data.get("title")
            if (len(title)<3) :
                raise(ValidationError({'title':'At least 3 character'}))
        except ValueError:
            raise(ValidationError({'title':'Dinh dang k dung'}))
        return super().create(request, *args, **kwargs)


class PostRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    lookup_field = 'id'
    serializer_class = PostSerializer

    def delete(self, request, *args, **kwargs):
        post_id = request.data.get('id')
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete('post_data_{}'.format(post_id))
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            from django.core.cache import cache
            post = response.data
            cache.set('post_data_{}'.format(post['id']), {
                'title': post['title'],
                'content': post['content'],
            })
        return response


class UserPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id',)
    pagination_class = UserPagination

    def get_queryset(self):
        return super().get_queryset()

class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id',)
    pagination_class = UserPagination

    def get_queryset(self):
        return super().get_queryset()