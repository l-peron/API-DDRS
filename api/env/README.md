# API

# Actions effectuées

Ci dessous une liste des commandes effectuées, en suivant le [Quickstart DRF](https://www.django-rest-framework.org/tutorial/quickstart/).

## Mise en place d'un projet Django

1. `python3 -m venv env` (Attention, sous Debian/Ubuntu il faut au préalable installer le package `python-venv`)
2. `source env/bin/activate`

*A partir de maintenant, nous sommes désormais dans un env. virtuel pour isoler les dépendances*

3. `pip install django` (`pip` doit être installé)
4. `pip install djangorestframework`
5. `django-admin startproject api .`
6. `cd api`
7. `django-admin startapp ddrsapp-api`

*On possède désormais une architecture basique de Django*

## Synchronisation de la base de données

`python manage.py migrate`

## Création de Serializers

On créera ici juste un serializer pour les users (pour l'instant, devra être fait pour chaque donnée envoyée/reçue).
