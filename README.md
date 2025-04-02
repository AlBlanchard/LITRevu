# LITReview

LITReview est une application web Django permettant aux utilisateurs de partager, commenter et suivre des critiques de livres et d'articles.  
Elle permet de publier des tickets pour demander une critique, d'y répondre, et de suivre l'activité de ses abonnements via un flux.

## Fonctionnalités

- Inscription et authentification sécurisée
- Création de tickets pour demander une critique
- Rédaction de critiques sur ses propres billets ou ceux des utilisateurs suivis
- Flux personnalisé avec les billets et critiques des abonnements
- Système d’abonnement et de désabonnement à des utilisateurs
- Interface responsive et accessible (design mobile first)
- Interface d’administration Django personnalisée

## Installation

**1. Clonez le dépôt :**

```bash
git clone https://github.com/AlBlanchard/LITRevu.git
cd litreview
```

**2. Créez et activez l'environnement virtuel**

```bash
python -m venv env
```
*Sous Windows*
```bash
env\Scripts\activate
```
*Sous Mac/Linux*
```bash
source env/bin/activate 
```

**3. Installez les dépendances**

```bash
pip install -r requirements.txt
```

**4. Appliquez les migrations**

```bash
python manage.py migrate
```

**5. Créez un super user**

```bash
python manage.py createsuperuser
```

**6. Lancez le serveur**

```bash
python manage.py runserver
```

Vous n'aurez plus qu'à ouvrir l'url locale indiquée dans votre terminale, habituellement : [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Super User

Pour accéder à l'interface administrateur, connectez vous sur la page login classique avez vos identifiants Super User précédemment créés. 

Une fois connecté, rendez vous sur l'url locale :
http://127.0.0.1:8000/admin/