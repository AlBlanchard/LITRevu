
# LITRevu

  

LITRevu est une application web Django permettant aux utilisateurs de partager, commenter et suivre des critiques de livres et d'articles.

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
git  clone  https://github.com/AlBlanchard/LITRevu.git

cd  litrevu
```

  

**2. Créez et activez l'environnement virtuel**

  

```bash
python  -m  venv  env
```

*Sous Windows*

```bash
env\Scripts\activate
```

*Sous Mac/Linux*

```bash
source  env/bin/activate
```

  

**3. Installez les dépendances**

  

```bash
pip  install  -r  requirements.txt
```

  

**4. Appliquez les migrations**

  

```bash
python  manage.py  migrate
```

  

**5. Créez un fichier .env à la racine du projet**

  

Notez dans le fichier :

```bash
# .env

SECRET_KEY=VOTRE_CLEF_SECRETE

DEBUG=True
```

Vous pouvez utiliser ce site pour générer une clef rapidement

https://djecrety.ir/

  

Faites attention à ne pas divulguer votre clef sur github ou ailleurs.

Pensez à désactiver le DEBUG pour le déploiement.
  

**7. Lancez le serveur**

  

```bash
python  manage.py  runserver
```

  

Vous n'aurez plus qu'à ouvrir l'url locale indiquée dans votre terminale, habituellement : [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Démo

Une base de données accompagne le repository. Celle-ci comporte plusieurs utilisateurs et post.

1. Accès aux utilisateurs pré enregistrés

> Login : **Admin**
>
> Mot de passe : **django10**

*Il s'agit d'un super user*


> Login : **User2**
>
> Mot de passe : **django20**

## Super User

 **Pour créer un nouveau super user**

```bash
python  manage.py  createsuperuser
```

Pour accéder à l'interface administrateur, connectez vous sur la page login classique avez vos identifiants Super User précédemment créés ou vous pouvez utiliser l'Admin préenregistré pour la démo.

Une fois connecté, rendez vous sur l'url locale :

http://127.0.0.1:8000/admin/

## Cleanup images
  
**Des images inutilisées peuvent parfois rester après la suppression d’un post.**  
Normalement, ces images sont supprimées automatiquement grâce à un signal défini dans `signals.py`.  
Cependant, si ce mécanisme ne fonctionne pas comme prévu, vous pouvez exécuter la commande suivante dans la console :

```bash
python manage.py cleanup_images
```