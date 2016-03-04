# Requirements
- A working mysql setup
- A working redis setup
- python3.5

# Installation
## Database

Sqlite is not supported.
To create a mysql database, use:
```
CREATE DATABASE my_database CHARACTER SET utf8;
```


## Venv
```
pyvenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Migrations
```
./manage.py migrate
```

## SuperUser creation
```
./manage.py createsuperuser
```

You should now be able to connect and admin the website !
