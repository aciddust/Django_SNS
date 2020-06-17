from django.urls import include, path, re_path
from rest_framework import routers

from apis.v1 import (
    UserCreateView, UserLoginView, UserLogoutView,
    ContentCreateView, ContentDeleteView,
    RelationCreateView, RelationDeleteView,
    AccountImageUpdateView, AccountProfileUpdateView,
    UserGetView, CommentGetView, CommentPostView,
    LikeCreateView, LikeDeleteView, LikeGetView,
)

from apis.v2 import (
    UserViewSet, CommentViewSet, CommentReverseViewSet,
)

urlpatterns = [
    path('v1/users/login/', UserLoginView.as_view(), name='apis_v1_user_login'),
    path('v1/users/logout/', UserLogoutView.as_view(), name='apis_v1_user_logout'),
    path('v1/users/create/', UserCreateView.as_view(), name='apis_v1_user_create'),
    path('v1/users/get/', UserGetView.as_view(), name='apis_v1_user_get'),
    re_path('^v2/users/get/(?P<name>.+)/$', UserViewSet.as_view()),

    path('v1/accounts/image/update/', AccountImageUpdateView.as_view(), name='apis_v1_account_image_update'),
    path('v1/accounts/profile/update/', AccountProfileUpdateView.as_view(), name='apis_v1_account_profile_update'),

    path('v1/contents/create/', ContentCreateView.as_view(), name='apis_v1_content_create'),
    path('v1/contents/delete/', ContentDeleteView.as_view(), name='apis_v1_content_delete'),

    path('v1/like/get/', LikeGetView.as_view(), name='apis_v1_like_get'),
    path('v1/like/create/', LikeCreateView.as_view(), name='apis_v1_like_create'),
    path('v1/like/delete/', LikeDeleteView.as_view(), name='apis_v1_like_delete'),

    path('v1/comments/get/', CommentGetView.as_view(), name='apis_v1_comment_get'),
    re_path('^v2/comments/get/(?P<post>.+)/$', CommentViewSet.as_view()),
    re_path('^v2/comments/reverse/get/(?P<post>.+)/$', CommentReverseViewSet.as_view()),
    path('v1/comments/post/', CommentPostView.as_view(), name='apis_v1_comment_post'),

    path('v1/relations/create/', RelationCreateView.as_view(), name='apis_v1_relation_create'),
    path('v1/relations/delete/', RelationDeleteView.as_view(), name='apis_v1_relation_delete'),
]
