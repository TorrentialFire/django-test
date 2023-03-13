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

## Template customization

```bash 
# Locate the template directory for Django
python -c "import django; print(django.__path__)"

# Copy the template to be modified into the project-wide templates dir
cp /home/zero/.virtualenvs/local-django/lib/python3.10/site-packages/django/contrib/admin/templates/admin/base_site.html ./templates/admin/base_site.html 
```

## LDAP

```bash
# Ubuntu 22.04 (openldap may already be installed, but this command installs)
sudo apt-get update && sudo apt-get install libldap-2.5-0 libldap-dev -y

# Required libraries for python-ldap
sudo apt-get update && sudo apt-get install libsasl2-dev ldap-utils -y
```

Add the following to `requirements.txt`:

```
python-ldap>=3.0
django-auth-ldap
```

Test using a local ldap server deployed via docker:
[https://github.com/rroemhild/docker-test-openldap](https://github.com/rroemhild/docker-test-openldap)


`project/settings.py`:
```python
import ldap
from django_auth_ldap.config import LDAPSearch

#...

# Begin Authentication and LDAP Support

AUTHENTICATION_BACKENDS = [
    "django_auth_ldap.backend.LDAPBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# Set up LDAP server and user search parameters.
AUTH_LDAP_SERVER_URI = "ldap://localhost:10389"
AUTH_LDAP_BIND_DN = "cn=admin,dc=planetexpress,dc=com"
AUTH_LDAP_BIND_PASSWORD = "GoodNewsEveryone"
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    "ou=people,dc=planetexpress,dc=com",
    ldap.SCOPE_SUBTREE,
    "(uid=%(user)s)"
)

# Set up the basic group parameters.
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    'ou=people,dc=planetexpress,dc=com',
    ldap.SCOPE_SUBTREE,
    '(objectClass=groupOfNames)',
)
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr='cn')

# Populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
    'first_name': 'givenName',
    'last_name': 'sn',
    'email': 'mail',
}

# Simple group restrictions
AUTH_LDAP_REQUIRE_GROUP = 'cn=admin_staff,ou=people,dc=planetexpress,dc=com'
AUTH_LDAP_DENY_GROUP = 'cn=ship_crew,ou=people,dc=planetexpress,dc=com'

# This is the default, but I like to be explicit.
AUTH_LDAP_ALWAYS_UPDATE_USER = True

# Use LDAP group membership to calculate group permissions.
AUTH_LDAP_FIND_GROUP_PERMS = True

# Important boolean fields defined by group membership
# Values in this dictionary may be simple DNs (as strings), lists or tuples of DNs, or LDAPGroupQuery instances. Lists are converted to queries joined by |.
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    #"is_active": "cn=active,ou=groups,dc=example,dc=com",
    "is_staff": (
        LDAPGroupQuery("cn=admin_staff,ou=people,dc=planetexpress,dc=com")
        #| LDAPGroupQuery("cn=admin,ou=groups,dc=example,dc=com")
    ),
    "is_superuser": "cn=admin_staff,ou=people,dc=planetexpress,dc=com",
}

# Cache distinguished names and group memberships for an hour to minimize
# LDAP traffic.
AUTH_LDAP_CACHE_TIMEOUT = 3600

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "handlers": {"console": {"class": "logging.StreamHandler"}},
#     "loggers": {"django_auth_ldap": {"level": "DEBUG", "handlers": ["console"]}},
# }

# End LDAP configuration
```

Login as user `professor` with password `professor`, or `hermes`/`hermes`. 

Attempting to login as a member of `ship_crew` will fail on the admin site.