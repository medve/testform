from django.contrib.auth import (
    authenticate, get_user_model
)

from models import MultiphoneUser

UserModel = MultiphoneUser

def authenticate_by_phone(self, phone, password, 
                                 *args, **kwargs):  
    try:
        user = UserModel.objects.get_user_by_phone(phone)
        if user.check_password(password):
            return user
    #got from Django's authentication
    except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)
