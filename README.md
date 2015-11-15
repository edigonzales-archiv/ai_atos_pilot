# Installation

OS: Xubuntu 14.04.3

## virtualenv

### virtualenv installieren

```
sudo apt-get install python-pip
sudo pip install virtualenv virtualenvwrapper
```

In `.bashrc` einfügen:

```
if [ -f /usr/local/bin/virtualenvwrapper.sh ]; then
    export WORKON_HOME=$HOME/.virtualenvs
    source /usr/local/bin/virtualenvwrapper.sh
fi
```

Falls nötig einmalig (zum Weiterarbeiten) `source ~/.bashrc` ausführen.

### virtualenv einrichten

Projekt klonen:

```
git clone https://edigonzales@bitbucket.org/edigonzales/ai_atos_pilot.git
```

In das `ai_atos_pilot/services/` Verzeichnis wechseln:


```
virtualenv venv
source venv/bin/activate
pip install flask
pip install pytz
```

## Apache

Es wird zusätzlich das `mod_wsgi` Modul benötigt:

```
sudo apt-get install libapache2-mod-wsgi 
sudo a2enmod wsgi 
```

**ANPASSEN!!**

```
WSGIScriptAlias /services /home/stefan/Projekte/ai_atos_pilot/services/wsgi/flask.wsgi
WSGIScriptReloading On

<Directory /home/stefan/Projekte/ai_atos_pilot/services/wsgi>
    Order deny,allow
    Allow from all
</Directory>
```

# Tipps & Tricks

## Develop mode (local web server)

Als erste Zeile in von `run.py`: `#!venv/bin/python`

Und zu guter Letzt:

```
if __name__ == '__main__':
    app.run(debug=True)
```

# Meta-DB

Die AI hat noch keine Meta-DB. Für das Pilotprojekt wird eine kleine SQLite-Datenbank erstellt mit den notwendingen Informationen, um AtOS bedienen zu können.
