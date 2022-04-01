from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from reviews.models import Review, Title, Genre, Categories

from .filters import TitleGenreFilter
from .mixins import CreateDestroyListViewSet
from .permissions import (IsAdminOrReadOnly,
                          IsAuthenticatedUserModeratorAdminCreateObject)
from .serializers import (CommentSerializer,
                          ReviewSerializer,
                          TitleSerializer,
                          TitleCreateSerializer,
                          CategoriesSerializer,
                          GenreSerializer)
from .throttling import PostUserRateThrottle


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedUserModeratorAdminCreateObject]
    throttle_classes = [PostUserRateThrottle]

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
    permission_classes = [IsAuthenticatedUserModeratorAdminCreateObject]

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
