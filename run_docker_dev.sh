#!/bin/bash
docker run -n gestioneide-dev --rm -it -v $PWD:/app -p 8000:8000 gestioneide:dev ./manage.py runserver 0.0.0.0:8000
