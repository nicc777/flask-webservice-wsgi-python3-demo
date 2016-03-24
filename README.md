# Flask Web Services Example on Linux with Apache 2 and WSGI

## Introduction

I have battled through a number of tutorials to try and get a basic Flask web services application going, using the following stack:

* Linux (Debian)
* Apache 2
* WSGI
* Python 3

In addition, I would like to run the application in a virtual environment.

Have a look further down below at the section for "Further Reading" of the resources I have consulted in order to arrive at this demo application.

## Preparing the Environment

I am not going to go over the installation of Linux. For the purpose of this guide, I have used Debian 8 (jessie) and I assume you have a running version which are patched.

I further assume you know how to install packages using the "apt" utilities.

I am also assuming you are logged in as root. Some users may wish to stick with the "sudo" command - it's your choice.

Use the following commands as a guide:

```
# sudo apt-get install apache2 python3 python3-pip python3-virtualenv libapache2-mod-wsgi-py3 git
# sudo update-alternatives --config python
```

The last command allows you to set Python3 as a default option. You can then easily test:

```
# python --version
Python 3.4.2
```

The minimum require software should now be installed and your default python interpreter should point to python 3.

## Install from GitHub

Change into /tmp and run the following commands (I am not going to explain every single step):

```
# git clone https://github.com/nicc777/flask-webservice-wsgi-python3-demo.git
# mkdir /opt/fwsdemo
# cp flask-webservice-wsgi-python3-demo/opt/fwsdemo/app.wsgi /opt/fwsdemo/
# cp flask-webservice-wsgi-python3-demo/apache_conf/fwsdemo.conf /etc/apache2/sites-available/
# cd flask-webservice-wsgi-python3-demo/
# python setup.py sdist
# cd /opt/fwsdemo/
# virtualenv --python=python3 venv
# . venv/bin/activate
(venv)# pip install /tmp/flask-webservice-wsgi-python3-demo/dist/fwsdemo-0.0.1.tar.gz
```

Now a quick test:

```
(venv)# python
Python 3.4.2 (default, Oct  8 2014, 10:45:20)
[GCC 4.9.1] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from fwsdemo import app
Using dbString=sqlite:///test2.db
>>>
(venv)# rm -vf test2.db
removed ‘test2.db’
(venv)# deactivate
#
```

Prepare the directory permissions (required for the DB - may not be required in most other cases):

```
# cd /opt
# chown -R www-data.www-data fwsdemo/
# chmod 770 fwsdemo/
```

Enable the Apache config:

```
# a2ensite fwsdemo.conf
Enabling site fwsdemo.
To activate the new configuration, you need to run:
  service apache2 reload
# service apache2 reload
```

## Testing

Simple test from the local machine:

```
# curl http://localhost/
{"userCount": 0}
```

Use SQLite to add some data for more tests:

```
# sqlite3 /opt/fwsdemo/test.db
SQLite version 3.8.7.1 2014-10-29 13:59:56
Enter ".help" for usage hints.
sqlite> .schema users
CREATE TABLE users (
	id INTEGER NOT NULL,
	name VARCHAR(50),
	email VARCHAR(120),
	PRIMARY KEY (id),
	UNIQUE (name),
	UNIQUE (email)
);
sqlite> insert into users ( name, email ) values ( 'Person1', 'p1@example.tld' );
sqlite> insert into users ( name, email ) values ( 'Person2', 'p2@example.tld' );
sqlite> select * from users;
1|Person1|p1@example.tld
2|Person2|p2@example.tld
sqlite>
# curl http://localhost/
{"userCount": 2}
```

## Running the Unit Tests

You can also run unit tests. Below is an example session to illustrate how to accomplish this. Note that some output have been omitted.

```
# cd /tmp
# mkdir unittest
# cd unittest/
# virtualenv --python=python3 venv
# . venv/bin/activate
(venv)# git clone https://github.com/nicc777/flask-webservice-wsgi-python3-demo.git
(venv)# cd flask-webservice-wsgi-python3-demo/
(venv)# pip install flask sqlalchemy flask-restful
(venv)# python -m unittest
Using dbString=sqlite:///unittests.db
setUpModule
  setUpClass
       setUp
[<User 'person1'>, <User 'person2'>]
  class 1 test 1
       tearDown
.       setUp
WARNING: Couldn't create new test data.
  class 1 test 2
       tearDown
.  tearDownClass
tearDownModule

----------------------------------------------------------------------
Ran 2 tests in 0.026s

OK
```

## Running Unit Tests with Coverage

You can also get coverage reporting on the unit tests. Below is an example that produces a coverage report. The last command will also create a HTML report:

```
# cd /tmp
# git clone https://github.com/nicc777/flask-webservice-wsgi-python3-demo.git
# cd flask-webservice-wsgi-python3-demo/
# virtualenv --python=python3 venv
# python setup.py sdist
# . venv/bin/activate
(venv)# pip install dist/fwsdemo-0.0.1.tar.gz coverage
(venv)# coverage run -m unittest
(venv)# coverage report --include='fwsdemo/*.py' --omit='*/__init__.py' -m
Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
fwsdemo/database.py      13      0   100%   
fwsdemo/models.py        12      0   100%   
---------------------------------------------------
TOTAL                    25      0   100%   
(venv)# coverage html -d report_html --include='fwsdemo/*.py' --omit='*/__init__.py'
```

## Further Reading

There were many resources I have used in putting this tutorial together, so overall I want to thank all the Python contributors on sites like stackoverflow which I use intensively almost on a daily basis - you guys rock! I wish I took down all the pages I used for this demo, but unfortunately I did not track it from the start, so I will just acknowledge for now the main non-stackoverflow resources I used.

1. The first site I used was by [Tero Karvinen](http://terokarvinen.com/2016/deploy-flask-python3-on-apache2-ubuntu "Deploy Flask & Python3 on Apache2 & Ubuntu")
2. Then there was a good WSGI tutorial (python 2 based) from [Christian Hettlage](http://software.saao.ac.za/2014/10/29/deploying-a-flask-application-on-apache/ "Deploying a Flask application on Apache")
3. Of course there is the official [Flask Site](http://flask.pocoo.org/docs/0.10/ "Flask")

I also need to mention two books I used extensively to learn Flask and which put me on this journey in the first place:

1. The first book was [Flask Web Development](http://www.flaskbook.com "Flask Web Development") by [Miguel Grinberg](https://github.com/miguelgrinberg "GitHub")
2. The second book I used extensively was [Essential SQLAlchemy](http://shop.oreilly.com/product/0636920035800.do "Essential SQLAlchemy")


[About Me](about.me/nico.coetzee "About Nico Coetzee")
