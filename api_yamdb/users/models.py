from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, TextField


# class User(AbstractUser):
#     """Переопределенная модель User с дополнительными полями."""
#     USER = 'user'
#     MODERATOR = 'moderator'
#     ADMIN = 'admin'
#     ROLE_CHOICES = (
#         (USER, USER)
#         (MODERATOR, MODERATOR),
#         (ADMIN, ADMIN),
#     )
#     bio = TextField(
#         blank=True,
#         verbose_name='Информация о пользователе'
#     )
#     role = CharField(
#         max_length=20,
#         choices=ROLE_CHOICES,
#         default=USER,
#         verbose_name='Роль'
#     )
class CustomUser(AbstractUser):
    pass

    def str(self):
        return self.username
