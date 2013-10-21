GUTS_website
============
TODO:
* Email sending status - how many emails sent out of how many
* Email sending - respect unsubscribed

* Event photos upload admin interface (take from event creating?)
* Test facebook integration on event creating
* Facebook integration on event editing
* ics generator/parser (for one click add event to GCal and others)

### INSTALL
1. Install dependencies
```bash
sudo apt-get install git mysql-server python-pip
```

2. Install flask and other python modules:
```bash
pip install flask-sqlalchemy flask-wtf flask-login requests python-mysql
```

### CONFIGURE
1. Create mysql user and database:
```mysql
create database guts;
create user 'guts'@'localhost' identified by 'password';
grant all privileges on guts.* to 'guts'@'localhost';
```

2. Create a copy of the `guts_website/sensitive.py.fake`:
```bash
cp guts_website/sensitive.py{.fake,}
```

3. Change the following variables in `guts_website/sensitive.py` to match your settings:
 * `DB_PASSWORD`
 * `ADMIN_USER`
 * `ADMIN_PASSWORD`

4. Create tables from the models:
```python
from guts_website import db, models
db.create_all()
```

### USE
#### Running the application
```bash
python run.py
```

#### Adding new technology
```python
project = models.Project("title", "author", "contact", "web address", "description", "icon")
project.technologies.append(models.Technology("flask", "http://flask.pocoo.org/"))
db.session.add(project);
db.session.commit()
```

### CONTRIBUTE
First of all, thank you!

Fork this repository, do your things in a new branch, commit not too small and not too big changes and just send me a pull request. More about the process [here](https://help.github.com/articles/using-pull-requests).
