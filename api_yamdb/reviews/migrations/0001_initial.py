# Generated by Django 2.2.16 on 2022-03-30 20:12

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import reviews.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=50, verbose_name='Название')),
                ('slug', models.SlugField(unique=True, verbose_name='slug')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=50, verbose_name='Название')),
                ('slug', models.SlugField(unique=True, verbose_name='slug')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(db_index=True, max_length=50, verbose_name='Название')),
                ('year', models.IntegerField(blank=True, validators=[django.core.validators.MaxValueValidator(2022, message='Год выпуска не может быть позже текущего года')])),
                ('description', models.CharField(blank=True, max_length=200, null=True, verbose_name='Описание')),
                ('categories', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.Categories', verbose_name='Категория')),
                ('genre', models.ManyToManyField(blank=True, db_index=True, related_name='titles', to='reviews.Genre', verbose_name='Жанр')),
            ],
            options={
                'ordering': ('-year',),
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('text', models.TextField(help_text='Add review', max_length=50000, validators=[reviews.validators.validate_emptiness], verbose_name='Review text')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_author', to=settings.AUTH_USER_MODEL, verbose_name='user')),
                ('score', models.ForeignKey(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9')], on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='rank')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_title', to='reviews.Title', verbose_name='Review')),
            ],
            options={
                'ordering': ['-pub_date', '-pk'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('text', models.TextField(help_text='Add review', max_length=50000, validators=[reviews.validators.validate_emptiness], verbose_name='comments')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_author', to=settings.AUTH_USER_MODEL, verbose_name='user')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_review', to='reviews.Review', verbose_name='Comment')),
                ('title', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='changename_title', to='reviews.Title', verbose_name='Review')),
            ],
            options={
                'ordering': ['-pub_date', '-pk'],
            },
        ),
    ]
