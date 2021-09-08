# gestioneide

## Introducción


## Instalación

```
apt install python3 python-is-python3

```

```
git clone https://github.com/Etxea/gestioneide.git
cd gestioneide
git checkout -b nuevotema remotes/origin/nuevotema
mkdir gestioneide/site_media
chown gestioneide/www-data site_media
virtualenv .
source ./bin/activate
sudo apt-get install libmysqlclient-dev libjpeg-dev
#Debian 9
sudo apt-get install libmariadbclient-dev libjpeg-dev

#Runnig database in docker
docker run --name mysql_55 -e MYSQL_ROOT_PASSWORD=mypass -d -p 3306:3306 mysql:5.5

pip install -r requirements.txt
./manage.py migrate
./manage.py createsuperuser
./manage.py loaddata gestioneide
./manage.py festivos calendario_laboral_2016.csv
./manage.py collectstatic
```

### Plesk

https://support.plesk.com/hc/en-us/articles/115002701209-How-to-install-Django-applications-in-Plesk-


## Getting Started

