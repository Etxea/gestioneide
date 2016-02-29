# gestioneide

## Instalación

git clone https://github.com/Etxea/gestioneide.git
cd gestioneide
git checkout -b nuevotema remotes/origin/master
virtualenv .
source ./bin/activate
sudo apt-get install libmysqlclient-dev
pip install -r requirements.txt
./manage-py migrate


## Getting Started

Make sure you are using a virtual environment of some sort (e.g. `virtualenv` or
`pyenv`).

```
pip install -r requirements.txt
./manage.py migrate
./manage.py loaddata sites
./manage.py runserver
```
