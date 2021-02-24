#  DEMO Version - Universal Electronic Medical Report System( Django )

#  How to set up this application
##  Set up the Database

You can reference the following this [link](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04)

**Step 1:** Install PostgreSQL

**Step 2:** Create user and database on PostgreSQL

##  Install necessary packages

**Step 1:** git clone this repo

**Step 2:** cd to the cloned repo

**Step 3:** install python library with `pip install -r config/requirements.txt`

**Step 4:** setup user and database in settigs **medi/settings/local_settings.py**

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '<DB Name>',
        'USER': '<DB Username>',
        'PASSWORD': '<DB Password>',
        'HOST': '',
    }
}
```

**Step 5:** migrate database with `python manage_local.py migrate`

#  Import inital data into the database ( only one time )

**psql -U [USER] [DATABASE] < initial_data/initial.sql**


#  Run the application

**python manage_local.py runserver**
