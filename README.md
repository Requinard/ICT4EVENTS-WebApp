#ICT4Event Web app

![build-passing](https://travis-ci.org/Requinard/ICT4EVENTS-WebApp.svg?branch=master)
-------------------------

An app for managing events. Created for Fontys Hogeschool as a Semester Project.

## Requirements

- Python(2.7, 3.3, 3.4)
- A server

## Preparing on windows

- DDownload psycopgs [here](http://www.stickpeople.com/projects/python/win-psycopg/)

## Setting up the ldap server

- Install slapd
- install phpldapadmin
- Go to /usr/share/phpldapadmin/templates/creation/
- Open posixAccount.xml
- Add the following text

    \<attribute id="mail">
            <display>Email</display>
    \</attribute>

- Go to /etc/ldap/scheme/
- Open nis.schema and add the following lines

attributetype ( 1.3.6.1.1.1.1.3 NAME 'mail'
        DESC 'a users email adress'
        EQUALITY caseExactIA5Match
        SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 SINGLE-VALUE )



## How to run

- First, make sure you already have python
- Install the requirements with "pip install -r requirements.txt"
- Run the test with "python manage.py test"
- After the tests complete, run "python manage.py runserver 0.0.0.0:8000"

You are now running a local dev server. Adjust settings in settings.py to customize it.

You can find the webserver [localhost:8000](http://localhost:8000)