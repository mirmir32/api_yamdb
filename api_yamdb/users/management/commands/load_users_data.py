import os
from csv import DictReader
from uuid import uuid4

from django.core.management import BaseCommand

from users.models import CustomUser

ALREDY_LOADED_ERROR_MESSAGE = ('delete the db.sqlite3 file before reload data'
                               'from the CSV file')


class Command(BaseCommand):
    # Show this when the user types help
    help = 'Loads data from users.csv'

    def handle(self, *args, **options):
        # Show this if the data already exist in the database
        if (
            CustomUser.objects.count() > 1
            and not
            CustomUser.objects.filter(id=1).exists()
        ):
            print('Users data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        # Show this before loading the data into the database
        print('Loading users data')
        # Code to load the data into database
        try:
            reader = DictReader(open('users.csv'))
            for row in reader:
                # id,username,email,role,bio,first_name,last_name
                print(row['id'])
                user = CustomUser(
                    id=row['id'],
                    email=row['email'],
                    username=row['username'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    confirmation_code=str(uuid4()),
                )
                user.save()
        except Exception:
            print(os.getcwd())
