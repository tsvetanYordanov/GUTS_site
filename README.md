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
sudo apt-get install git mysql-server apache2 python-pip libapache2-mod-wsgi
```

2. Install flask and other python modules:
```bash
pip install flask-sqlalchemy flask-wtf flask-login requests python-mysql
```

3. Assuming cloned to /var/www, add to /etc/apache2/httpd.conf:
```apache
    <VirtualHost *>
        WSGIDaemonProcess application user=www-data group=www-data threads=5
        WSGIScriptAlias / /var/www/GUTS_website/guts.wsgi

        <Directory /var/www/GUTS_website>
            WSGIProcessGroup application
            WSGIApplicationGroup %{GLOBAL}
            Order deny,allow
            Allow from all
        </Directory>
    </VirtualHost>
```

4. Create mysql user and database:
```mysql
create database guts;
create user 'guts'@'localhost' identified by 'password';
grant all privileges on guts.* to 'guts'@'localhost';
```

5. Create tables from the models:
```python
>>>> from guts_website import db, models
>>>> db.create_all()
```

### CONFIGURE
The file `guts_website/sensitive.py` contains passwords which are not the same as in the production environment for obvious reasons. You can play with the sandbox page as much as you would like.

### USE
To add new technology:
```python
project = models.Project("title", "author", "contact", "web address", "description", "icon")
project.technologies.append(models.Technology("flask", "http://flask.pocoo.org/"))
db.session.add(project);
db.session.commit()
```

### CONTRIBUTE
First of all, thank you!

Fork this repository, do your things in a new branch, commit not too small and not too big changes and just send me a pull request. More about the process [here](https://help.github.com/articles/using-pull-requests).
