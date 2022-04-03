from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import filters, viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response

from reviews.models import Review, Title, Genre, Categories
from .filters import TitleGenreFilter
from .mixins import CreateDestroyListViewSet
from .permissions import (IsAdminOrReadOnly,
                          IsObjectOwnerModeratorAdminOrReadOnly,
                          IsAdmin)
from .serializers import (CommentSerializer,
                          ReviewSerializer,
                          TitleSerializer,
                          TitleCreateSerializer,
                          CategoriesSerializer,
                          GenreSerializer,
                          UserSerializer,
                          TokenSerializer,
                          SignUpSerializer,
                          AccountSerializer)
from .throttling import PostUserRateThrottle
from users.models import CustomUser


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = [
        IsObjectOwnerModeratorAdminOrReadOnly | IsAuthenticatedOrReadOnly]
    throttle_classes = (PostUserRateThrottle,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        new_queryset = title.review_title.all()
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)
        return title.review_title.all()

    def perform_update(self, serializer):
        title = get_object_or_404(Title,
                                  id=self.kwargs['title_id'],
                                  review=self.kwargs['review_id'])
        serializer.save(author=self.request.user, title=title)
        return title.review_title.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = (
        IsObjectOwnerModeratorAdminOrReadOnly,
        IsAuthenticatedOrReadOnly,
    )

    def get_queryset(self):
        review = get_object_or_404(Review,
                                   id=self.kwargs['review_id'],
                                   title=self.kwargs['title_id'])
        queryset = review.comment_review.all()
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review,
                                   id=self.kwargs['review_id'],
                                   title=self.kwargs['title_id'])
        serializer.save(author=self.request.user,
                        review=review)
        return review.comment_review.all()

    def perform_update(self, serializer):
        review = get_object_or_404(Review,
                                   id=self.kwargs['review_id'],
                                   title=self.kwargs['title_id'],
                                   comment=self.kwargs['comment_id'])
        serializer.save(author=self.request.user,
                        review=review)
        return review.comment_review.all()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleGenreFilter

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return TitleCreateSerializer
        return TitleSerializer


class CategoriesViewSet(CreateDestroyListViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)


class GenreViewSet(CreateDestroyListViewSet):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = UserSerializer
    lookup_field = 'username'
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)

    @action(
        methods=('GET', 'PATCH',),
        detail=False,
        url_path='me',
        serializer_class=AccountSerializer,
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        user = get_object_or_404(CustomUser, pk=request.user.id)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    user = get_object_or_404(CustomUser, username=username)
    refresh = RefreshToken.for_user(user)
    return Response({'token': str(refresh.access_token)},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def sign_up(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    user, created = CustomUser.objects.get_or_create(
        username=username,
        email=email,
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Код подтвержения доступа Yamdb',
        message=f'Код подтвержения доступа: {confirmation_code}',
        from_email='admin@yamdb.com',
        recipient_list=(email,))
    return Response(
        serializer.data,
        status=status.HTTP_200_OK)
