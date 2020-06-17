from accounts.models import User
from contents.models import (Comment, )
from rest_framework import permissions, generics
from django_filters.rest_framework import DjangoFilterBackend

from .v2_serializer import (UserSerializer, CommentSerializer, CommentReverseSerializer)


class UserViewSet(generics.ListAPIView):
    
    serializer_class = UserSerializer
    permissions_classes = [permissions.IsAuthenticated]
    filter_backends = (DjangoFilterBackend, )
    filter_fields=('name',)

    def get_queryset(self):
        get_query = self.kwargs['name']
        queryset = get_query.split('&')
        queryset = { query.split('=')[0]:query.split('=')[1] for query in queryset }
                
        try:
            username = queryset['name']
            username_split = username.split(' ')

            user = User.objects.filter(name=username)
            user = user.union(User.objects.filter(name=username_split[0]))
            user = user.union(User.objects.filter(name__startswith=username))
            user = user.union(User.objects.filter(name__endswith=username))
        
            if len(username_split) > 1:
                user = user.union(User.objects.filter(name__endswith=username_split[-1]))
                user = user.union(User.objects.filter(name=username_split[-1]))
        except Exception as e:
            # queryset에 key(name)없을경우
            user = User.objects.filter(name='')
        return user
        

class CommentViewSet(generics.ListAPIView):

    serializer_class = CommentSerializer
    permissions_classes = [permissions.IsAuthenticated]
    filter_backends = (DjangoFilterBackend, )
    filter_fields=('comment',)

    def get_queryset(self):
        get_query = self.kwargs['post']
        queryset = get_query.split('&')
        queryset = { query.split('=')[0]:query.split('=')[1] for query in queryset }

        try:
            post_id = queryset['post']
            comments = Comment.objects.filter(content__id=int(post_id))
        except Exception as e:
            # 댓글 없음.
            pass
        
        return comments

        ## 돌아와서 comment api 요청부분 처리해.

class CommentReverseViewSet(generics.ListAPIView):

    serializer_class = CommentReverseSerializer
    permissions_classes = [permissions.IsAuthenticated]
    filter_backends = (DjangoFilterBackend, )
    filter_fields=('comment',)

    def get_queryset(self):
        get_query = self.kwargs['post']
        queryset = get_query.split('&')
        queryset = { query.split('=')[0]:query.split('=')[1] for query in queryset }

        try:
            post_id = queryset['post']
            comments = Comment.objects.filter(content__id=int(post_id)).order_by('-id')
        except Exception as e:
            # 댓글 없음.
            pass
        
        return comments

        ## 돌아와서 comment api 요청부분 처리해.