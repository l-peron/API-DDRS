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
6. `python3 manage.py startapp ddrsapp_api`

*On possède désormais une architecture basique de Django*

## Création des modèles

On créer ici un modèle utilisateur ***très*** basique, qui sert d'exemple de base pour développer tout le reste.

## Création des serializers

On créer pour chaque modèle un serializer (disponible sous `ddrs_api/serializers.py`), permettant de passer d'une modèle à sa version `JSON` et inversement. 

**Attention :** on le fait ici seulement pour les utilisateurs, mais cela doit aussi être fait pour toutes les données susceptibles d'être transférées.

## Création des vues

On créer des vues (ou entry-points) pour les différentes requêtes. On choisit pour l'exemple une vue permettant de lister les utilisateurs (`users/`), et une autre permettant de regarder un utilisateur en particulier (`users/<id>`). Les vues sont dans `ddrs_api/views.py` et les urls correspondantes dans `ddrs_api/urls.py`.
