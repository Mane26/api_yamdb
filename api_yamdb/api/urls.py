from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (APIUser, CategoryViewSet, CommentViewSet, GenreViewSet,
                    MyUserViewSet, ReviewViewSet, TitleViewSet,
                    UserViewSetForAdmin)

router = DefaultRouter()
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')
router.register(
    r'users', MyUserViewSet, basename='MyUserViewSet'
)

router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register('users', UserViewSetForAdmin, basename='users')


urlpatterns = [
    path('v1/auth/', include('users.urls')),
    path('v1/users/me/', APIUser.as_view(), name='me'),
    path('v1/', include(router.urls)),
]
