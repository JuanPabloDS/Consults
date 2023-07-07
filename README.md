# Consults


<h2 align="center">CONSULTS</h2>

## :scroll: Description

This is a website where you can register companies and the systems your company provides support for. Initially, the system was developed for the company I worked for, aiming to facilitate the search for companies and identify which systems they used. Additionally, you can register trainings, including the day, time, company, and the system used. 

This system was designed to serve companies that deal with electronic timekeeping systems, but it can be used by any other company in need of a company registration system.

## :rocket: Technologies

The technologies usage in this project is:
- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [JavaScript](https://www.javascript.com/)
- [Bootstrap](https://getbootstrap.com/)
- [JQuery](https://www.sqlite.org/)


##  :wrench: Setup
Clone this repository in your computer.
```
$ git clone https://github.com/JuanPabloDS/Consults.git
```
After, install python development package:

Ubuntu.
```shell
$ sudo apt-get install python-dev
```

Fedora.
```shell
$ sudo dnf install python3-devel
```

Inside the project directory, you need to create your virtual enviroment and active it:
```shell
$ python -m venv pyenv
$ source pyenv/bin/activate
```

Upgrade pip:
```shell
$ pip install -U pip
```

Run the command to install the env requirements:
```shell
$ pip install -r requirements.txt
```

Run the migrations:
```shell
$ python manage.py migrate
```

Create your Django User:
```shell
$ python manage.py createsuperuser
```

Start the application:
```shell
$ python manage.py runserver
```

Look the swagger accessing *http://localhost:8000*
Look the django-admin accessing *http://localhost:8000/admin* and use your superuser email and password.
