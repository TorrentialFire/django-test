

```bash
# mkvirtualenv local-django
workon local-django

# update apt
sudo apt-get update

# install python packages
pip install -r requirements.txt

# create the project
django-admin startproject mysite

# To run the django app
python manage.py collectstatic
python manage.py runmodwsgi --reload-on-changes

#python manage.py runmodwsgi --setup-only --port=80 \
#    --user www-data --group www-data \
#    --server-root=/etc/mod_wsgi-express-80

# generate migrations
django-admin makemigrations [app_label [app_label ...]]
# preview migration
django-admin sqlmigrate app_label migration_name
# apply migration
python manage.py migrate


```