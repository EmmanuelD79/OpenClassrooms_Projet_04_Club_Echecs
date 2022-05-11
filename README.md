# OpenClassrooms_Projet_04_Master_Chess

Ce projet est le quatrième de la formation Openclassrooms Développeur d'application PYTHON.
<br>Son but est de coder un gestionnaire de tournoi d'échecs avec l'utilisation d'une base de donnée TinyDb.<br>
Grâce à un menu sur le terminal, nous pouvons :
<br> - Créer des joueurs
<br> - Créer des tournois
<br> - Organiser un tournoi entier avec les tours et matches puis un classement
<br> - Modifier le classement d'un joueur
<br> - Afficher la liste des joueurs par ordre alphabétique ou par classement
<br> - Afficher la liste des tournois
<br> - Afficher la liste des tours d'un tournoi
<br> - Afficher la liste des matches d'un tournoi

## Pour commencer

cloner le projet à l'aide de votre terminal en tapant la commande :
<br> 

```

git clone https://github.com/EmmanuelD79/OpenClassrooms_Projet_04_Club_Echecs.git

```

### Pré-requis

créer un environnement virtuel à l'aide de votre terminal en tapant la commande:
	<br>  
```

python -m venv env

```

puis l'activer :
<br>sur windows :

```

.\env\scripts\activate

```


<br>sur mac et linux : 

```

source env/bin/activate

```


### Installation

Pour utiliser ce projet, il est nécessaire d'installer les modules du fichier requirements.txt.

<br>Pour installer automatiquement ces modules, vous pouvez utiliser dans votre terminal la commande suivante :
	<br> 
```

pip install -r requirements.txt

```

ou le faire manuellement en consultant le fichier requirements.txt en tapant sur votre terminal la commande :
```

cat requirements.txt

```
puis les installer un par un avec la commande :
```

pip install <nom du paquage>

``` 


## Démarrage

Pour démarrer le projet, vous devez aller dans le répertoire du projet et taper sur votre terminal la commande:
	<br> 
```
	
python main.py
	
```

Le menu principal de gestionnaire s'affiche et vous demande de choisir entre:
<br> - la gestion des tournois
<br> - la gestion des joueurs
<br> - le lancement ou reprise d'un tournoi 
<br>
<br>
Un fichier JSON nommé "db.json" sera créé dans le répertoire principal du programme pour le stockage des données.
<br>Un dossier flake-report est présent, nous pouvons y trouver un rapport flake8-html.
<br>Pour générer un rapport, vous devez taper la commande dans le terminal:
```
	
flake8
	
```
## Fabriqué avec

Python 3.9