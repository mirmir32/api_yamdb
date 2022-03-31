import datetime as dt

from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models

from .validators import validate_emptiness

RANK = settings.RANKS


class Categories(models.Model):
    name = models.TextField('Название', max_length=50)
    slug = models.SlugField('slug', unique=True, db_index=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.TextField('Название', max_length=50)
    slug = models.SlugField('slug', unique=True, db_index=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField('Название', max_length=50, db_index=True)
    year = models.IntegerField(
        blank=True,
        validators=[
            MaxValueValidator(
                dt.datetime.now().year,
                message='Год выпуска не может быть позже текущего года'
            )
        ]
    )
    categories = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        db_index=True,
        related_name='titles',
        verbose_name='Жанр'
    )
    description = models.CharField(
        'Описание',
        max_length=200,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('-year',)

    def __str__(self):
        return self.name


class CreatedModel(models.Model):
    """Abstract model automatically creating "pub_date"."""
    pub_date = models.DateTimeField(
        verbose_name='Created date',
        auto_now_add=True)

    class Meta:
        abstract = True


class Review(CreatedModel):
    """
    Review creates reviews on exact title which are linked to the title.
    """
    title = models.ForeignKey(
        Title,
        verbose_name='Review',
        on_delete=models.CASCADE,
        related_name='review_title'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='user',
        on_delete=models.CASCADE,
        related_name='review_author'
    )
    score = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='rank',
        choices=RANK,
        blank=False,
        null=False
    )
    text = models.TextField(
        max_length=50000,
        verbose_name='Review text',
        help_text='Add review',
        validators=[validate_emptiness],
        blank=False
    )

    class Meta:
        ordering = ['-pub_date', '-pk']

    def __str__(self) -> str:
        return self.text[:25]


class Comment(CreatedModel):
    """
    Resource comments: comments to some exact review.
    Comments are linked to the exact review.
    """
    title = models.ForeignKey(
        Title,
        verbose_name='Review',
        on_delete=models.CASCADE,
        related_name='changename_title',
        blank=True,
        null=True
    )
    review = models.ForeignKey(
        Review,
        verbose_name='Comment',
        on_delete=models.CASCADE,
        related_name='comment_review',
        blank=False,
        null=False
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='user',
        on_delete=models.CASCADE,
        related_name='comment_author'
    )
    text = models.TextField(
        max_length=50000,
        verbose_name='comments',
        help_text='Add review',
        validators=[validate_emptiness],
        blank=False
    )

    class Meta:
        ordering = ['-pub_date', '-pk']

    def __str__(self) -> str:
        return self.text[:15]
