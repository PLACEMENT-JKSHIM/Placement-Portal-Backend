set -o allexport
test -f .env && source .env
set +o allexport



python manage.py shell -c "import environ; env = environ.Env(); env.read_env(); from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(env.get_value('SUPERUSER_USERNAME').strip(), env.get_value('SUPERUSER_EMAIL').strip(), env.get_value('SUPERUSER_PASSWORD').strip())"