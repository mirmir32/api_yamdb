from django.db import models

from django.conf import settings
from users.models import User
from .validators import validate_emptiness

RANK = settings.RANKS


class CreatedModel(models.Model):
    """Abstract model automatically creating "created date"."""
    created = models.DateTimeField(
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
        related_name='reviews',
        blank=True,
        null=True
    )
    author = models.ForeignKey(
        User,
        verbose_name='user',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.ForeignKey(
        User,
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
        ordering = ['-created', '-pk']

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
        related_name='reviews',
        blank=True,
        null=True
    )
    review = models.ForeignKey(
        Review,
        verbose_name='Comment',
        on_delete=models.CASCADE,
        related_name='comments',
        blank=False,
        null=False
    )
    author = models.ForeignKey(
        User,
        verbose_name='user',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        max_length=50000,
        verbose_name='comments',
        help_text='Add review',
        validators=[validate_emptiness],
        blank=False
    )

    class Meta:
        ordering = ['-created', '-pk']

    def __str__(self) -> str:
        return self.text[:15]
