from mongoengine import Document, StringField, BooleanField

class MongoUser(Document):
    username = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)

    # Admin fields
    is_staff = BooleanField(default=False)
    is_superuser = BooleanField(default=False)

    meta = {'collection': 'users'}

    def __str__(self):
        return self.username
