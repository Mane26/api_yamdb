from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import filters, response, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from api import permissions
from api.filters import TitleFilter
from api.pagination import Pagination
from api.permissions import (IsAdmin, IsAdminOrReadOnly,
                             IsAuthorOrAdministratorOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             ForAdminSerializer, ForUserSerializer,
                             GenreSerializer, MyUserSerializer,
                             ReviewSerializer, TitleCreateSerializer,
                             TitleSerializer, TokenSerializer)
from api_yamdb.settings import DEFAULT_FROM_EMAIL
from reviews.models import Review
from titles.models import Category, Genre, Title
from users.models import User


class CommentViewSet(viewsets.ModelViewSet):
    """POST для всех авторизованных, PATCH для модеров, админов и автора."""
    permission_classes = (IsAuthorOrAdministratorOrReadOnly,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'),
                                   title__id=self.kwargs.get('title_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = int(self.kwargs.get('review_id'))
        review = get_object_or_404(Review, id=review_id)
        user = self.request.user
        serializer.save(author=user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    """POST для всех авторизованных, PATCH для модеров, админов и автора."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrAdministratorOrReadOnly,)

    def get_queryset(self):
        title = Title.objects.get(id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = int(self.kwargs.get('title_id'))
        title = get_object_or_404(Title, pk=title_id)
        user = self.request.user
        serializer.save(author=user, title=title)


class CustomMixin(ListModelMixin, CreateModelMixin, DestroyModelMixin,
                  viewsets.GenericViewSet):
    pass


class CategoryViewSet(CustomMixin):
    """API для работы с моделью категорий."""
    pagination_class = Pagination
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CustomMixin):
    """API для работы с моделью жанров."""
    pagination_class = Pagination
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """API для работы с моделью произведений."""
    pagination_class = Pagination
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = TitleSerializer
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    ordering_fields = ('name',)
    ordering = ('name',)

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleCreateSerializer
        return TitleSerializer


def create_confirmation_code_and_send_email(username):
    """Создаем confirmation code и отправляем по email"""
    user = get_object_or_404(User, username=username)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Confirmation code',
        message=f'Your confirmation code {confirmation_code}',
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False
    )


class APISignUp(APIView):
    """Регистрация пользователя"""
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = ForUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # создаем confirmation code и отправляем на почту
            create_confirmation_code_and_send_email(
                serializer.data['username'])
        return Response({
            'email': serializer.data['email'],
            'username': serializer.data['username']},
            status=status.HTTP_200_OK)


class APIUser(APIView):
    """Работа со своими данными для пользователя"""
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.user.username)
        serializer = ForUserSerializer(user, many=False)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.user.username)
        serializer = ForUserSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIToken(APIView):
    """Выдача токена"""
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data["username"]
        )

        if default_token_generator.check_token(
            user, serializer.validated_data["confirmation_code"]
        ):
            token = AccessToken.for_user(user)
            return Response({"token": str(token)}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_token(request):
    """Функция получения токена при регистрации."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)
    confirmation_code = serializer.validated_data.get(
        'confirmation_code'
    )
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return response.Response(
            {'token': str(token)}, status=status.HTTP_200_OK
        )
    return response.Response(
        {'confirmation_code': 'Неверный код подтверждения!'},
        status=status.HTTP_400_BAD_REQUEST
    )


class UserViewSetForAdmin(ModelViewSet):
    """Работа с пользователями для администратора"""
    queryset = User.objects.all()
    serializer_class = ForAdminSerializer
    # поиск по эндпоинту users/{username}/
    lookup_field = 'username'
    permission_classes = (permissions.IsAdmin, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )


class MyUserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'username'
    filter_backends = [DjangoFilterBackend]
    search_fields = ['user__username']

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        if request.method == 'GET':
            return Response(
                self.get_serializer(request.user).data,
                status=status.HTTP_200_OK,
            )
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)
