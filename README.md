# gestioneide

## Introducción


## Instalación

```
git clone https://github.com/Etxea/gestioneide.git
cd gestioneide
git checkout -b nuevotema remotes/origin/nuevotema
mkdir gestioneide/site_media
chown gestioneide/www-data site_media
virtualenv .
source ./bin/activate
sudo apt-get install libmysqlclient-dev libjpeg-dev
pip install -r requirements.txt
./manage.py migrate
./manage.py createsuperuser
./manage.py loaddata gestioneide
./manage.py festivos calendario_laboral_2016.csv
./manage.py collectstatic
```

## Getting Started

