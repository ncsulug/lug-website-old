# NC State LUG Website

## Prerequisites

- python >= 2.5
- pip
- virtualenv
- A database

## Getting Set Up

First, clone the code from Git and `cd` into the directory.

### Creating the environment

Create a virtual Python environment for the project.

    $ virtualenv --no-site-packages --distribute env
    $ source env/bin/activate

### Install requirements

Install all the packages you'll need for the site.

    $ pip install -r requirements.txt

### Configure project

Edit the local settings file for your environment.
(This file will not be checked in to the git repository.)

    $ cp lug_site/__local_settings.py lug_site/local_settings.py
    $ $EDITOR lug_site/local_settings.py

### Sync database

Create all the database tables etcetera.

    $ python manage.py syncdb

## Running a development server

Now, to actually see the site:

    $ python manage.py runserver

Open <http://localhost:8000/> in your browser.
Congratulations! You have a LUG Website!
