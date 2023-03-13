# Djano

## Basic Django commands

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

# Run the app more concisely
python manage.py collectstatic --noinput && python manage.py runmodwsgi --reload-on-changes

#python manage.py runmodwsgi --setup-only --port=80 \
#    --user www-data --group www-data \
#    --server-root=/etc/mod_wsgi-express-80

# generate migrations
django-admin makemigrations [app_label [app_label ...]]
# preview migration
django-admin sqlmigrate app_label migration_name
# apply migration
python manage.py migrate

# Interactive shell can be used for editing instances of models
python manage.py shell
```

## Interacting with Models (Shell)

Commands in shell mode for interacting with models:

```python
from polls.models import Choice, Question
Question.objects.all()

# Django provides a rich database lookup API that's entirely driven by
# keyword arguments.
Question.objects.filter(id=1)
Question.objects.filter(question_text__startswith='What')

# Get the question that was published this year.
from django.utils import timezone
current_year = timezone.now().year
Question.objects.get(pub_date__year=current_year)

# Request an ID that doesn't exist, this will raise an exception.
Question.objects.get(id=2)

# Lookup by a primary key is the most common case, so Django provides a
# shortcut for primary-key exact lookups.
# The following is identical to Question.objects.get(id=1).
Question.objects.get(pk=1)

# Make sure our custom method worked.
q = Question.objects.get(pk=1)
q.was_published_recently()

# Give the Question a couple of Choices. The create call constructs a new
# Choice object, does the INSERT statement, adds the choice to the set
# of available choices and returns the new Choice object. Django creates
# a set to hold the "other side" of a ForeignKey relation
# (e.g. a question's choice) which can be accessed via the API.
q = Question.objects.get(pk=1)

# Display any choices from the related object set -- none so far.
q.choice_set.all()

# Create three choices.
q.choice_set.create(choice_text='Not much', votes=0)
q.choice_set.create(choice_text='The sky', votes=0)
c = q.choice_set.create(choice_text='Just hacking again', votes=0)

# Choice objects have API access to their related Question objects.
c.question

# And vice versa: Question objects get access to Choice objects.
q.choice_set.all()
q.choice_set.count()

# The API automatically follows relationships as far as you need.
# Use double underscores to separate relationships.
# This works as many levels deep as you want; there's no limit.
# Find all Choices for any question whose pub_date is in this year
# (reusing the 'current_year' variable we created above).
Choice.objects.filter(question__pub_date__year=current_year)

# Let's delete one of the choices. Use delete() for that.
c.delete()
```

## User management

```bash
# create an admin user
python manage.py createsuperuser

# Goto http://<site_url>/admin
```