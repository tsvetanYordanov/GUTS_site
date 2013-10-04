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
<pre><code>
sudo apt-get install git mysql-server apache2 python-pip libapache2-mod-wsgi python-mysqldb
</code></pre>

2. Install flask and other python modules:
<pre><code>
pip install flask-sqlalchemy flask-wtf flask-login requests
</code></pre>

3. Assuming cloned to /var/www, add to /etc/apache2/httpd.conf:
<pre><code>
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
</code></pre>

4. Create mysql user and database:
<pre><code>
create database guts;
create user 'guts'@'localhost' identified by 'password';
grant all privileges on guts.* to 'guts'@'localhost';
</code></pre>

5. Create tables from the models:
<pre><code>
python
>>>> from guts_website import db, models
>>>> db.create_all()

To add new technology:
project = models.Project("website", "me", "www", "Hello world")
project.technologies.append(models.Technology("flask", "http://flask.pocoo.org/"))
db.session.add(project);
db.session.commit()
</code></pre>

### CONFIGURE
The file `guts_website/sensitive.py` contains passwords which are not the same as in the production environment for obvious reasons. You can play with the sandbox page as much as you would like.

### CONTRIBUTE
First of all, thank you!

Fork this repository, do your things in a new branch, commit not too small and not too big changes and just send me a pull request. More about the process [here](https://help.github.com/articles/using-pull-requests).
