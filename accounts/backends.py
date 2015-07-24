from django.contrib.auth.models import User, check_password

class AuthBackend:
    def authenticate(self, email=None, password=None):
        if email and password:
            try:
                user = User.objects.get(email=email)
                if not check_password(password, user.password):
                    return None
                return user
            except User.DoesNotExist:
                return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

