# Generated by Django 2.2.16 on 2022-04-05 15:27

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import reviews.validators


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20220403_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_author', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_review', to='reviews.Review', verbose_name='Отзыв'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(help_text='Add review', validators=[reviews.validators.validate_emptiness], verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='title',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='changename_title', to='reviews.Title', verbose_name='Произведение'),
        ),
        migrations.AlterField(
            model_name='review',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, message='Оценка не может быть меньше минимального значения.'), django.core.validators.MaxValueValidator(10, message='Оценка не может быть больше максимального значения.')], verbose_name='Оценка'),
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(help_text='Add review', validators=[reviews.validators.validate_emptiness], verbose_name='Отзыв'),
        ),
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_title', to='reviews.Title', verbose_name='Произведение'),
        ),
    ]
