

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
```