# SESSAYMENT APPS
An application that todo assesment for students and teachers with automated marking system.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites

What things you need to install the software and how to install them

```
Python ^3.9
Django ^4.0

```

## Installing and Running

A step by step series of examples that tell you how to get a development env running

1. Clone the repository

```
git clone
```

2. Build environment

```
# with poetry
poetry install
poetry shell

# with venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Run migrations

```
python sessayment/manage.py migrate
```

5. Run server

```
python sessayment/manage.py runserver
```
