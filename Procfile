release: pip install -r requirements.txt  && python manage.py makemigrations && python manage.py migrate
web: gunicorn blog_project.wsgi