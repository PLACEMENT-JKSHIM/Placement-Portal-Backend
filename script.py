import environ
from django.contrib.auth import get_user_model

env = environ.Env()
env.read_env()

User = get_user_model()
exists = User.objects.filter(is_superuser=True).exists()

if exists:
    print('Admin already exists')
else:
    User.objects.create_superuser(
        env.get_value('SUPERUSER_USERNAME').strip(),
        env.get_value('SUPERUSER_EMAIL').strip(),
        env.get_value('SUPERUSER_PASSWORD').strip()
    )