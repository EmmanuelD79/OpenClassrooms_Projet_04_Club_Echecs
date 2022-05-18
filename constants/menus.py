DICT_CREATE_PLAYER_MENU = {
    "titre": "Bienvenue dans le menu création d'un joueur",
    "id": ["Quel est l'identifiant du joueur ? ", "[0-9]{3}$"],
    "first_name": ["Quel est le prénom du joueur ? ", "^[A-Za-z-]+$"],
    "last_name": ["Quel est le nom du joueur ? ", "^[A-Za-z-]+$"],
    "date_of_birth": ["Quel est le date de naissance du joueur (jj/mm/aaaa) ? ",
                      "(3[01]|[12][0-9]|0?[1-9])/(1[0-2]|0?[1-9])/([0-9]{4})"],
    "sex": ["Quel est le sexe du joueur M ou F ? ", "(M|F){1}$"],
    "rank": ["Quel est le classement du joueur ? ", "[0-9]{1,2}$"]
}

DICT_CREATE_TOURNAMENT_MENU = {
    "titre": ["Bienvenue dans le menu création d'un tournoi", "DICT_TOURNAMENT_MENU"],
    "id": ["Quel est l'identifiant du tournoi ? ", "[0-9]{3}$"],
    "name": ["Quel est le nom du tournoi ?", "^[A-Za-z0-9-_*]+$"],
    "site": ["Quel est le nom du site ? ", "^[A-Za-z0-9-_*]+$"],
    "control_time": ["Quel controle du temps désirez-vous \n"
                     "1 : un bullet \n"
                     "2 : un blitz \n"
                     "3 : un coup rapide \n"
                     "Quel est votre choix ? ", "[1-3]{1}$"],
    "description": ["Voulez-vous ajouter une description ? ", ""]
}

DICT_SORT = {
    "titre": "Menu d'affichage de liste par tri",
    1: [" 1 - Affichage du tri en alpha", ""],
    2: [" 2 - Affichage du tri par classement ", ""],
    0: [" 0 - Revenir au menu précedent", ""],
}

DICT_UPDATE_RANK = {
    "titre": ["Bienvenue dans la mise à jour du classement d'un joueur", ""],
    "id": ["Quel est l'identifiant du joueur ? ", "[0-9]{3}$"],
    "rank": [" Veuillez saisir le nouveau classement pour le joueur %s %s \n"
             "son classement est actuellement : %s ?", "[0-9]{1,2}$"],
    "confirmation": ["Vous avez changé son classement de %s par %s\nvoulez-vous confirmer O/N ?",
                     "(O|N){1}$"],
    "save": ["Le classement du joueur %s %s a été modifié pour %s", ""]
}

DICT_UPDATE_SCORE = {
    "confirmation": ["Voulez-vous les mettre à jour ? O/N", "(O|N){1}$"],
    "score": ["Qui le gagnant de ce match 1 / N / 2 ?", "(1|N|2){1}$"]
}

DICT_RUN_TOURNAMENT = {
    "titre": ["Bienvenue dans le menu de lancement d'un tournoi", ""],
    "id": ["Quel est l'identifiant du tournoi ? ", "[0-9]{3}$"],
}

DICT_START_MENU = {
    "titre": "Bienvenue dans le menu principal de la gestion de tournois d'échecs",
    1: [" 1 - Gérer les tournois", "setattr(self, 'dict_menu', DICT_TOURNAMENT_MENU)"],
    2: [" 2 - Gérer les joueurs", "setattr(self, 'dict_menu', DICT_ACTORS_MENU)"],
    3: [" 3 - Lancer/ reprendre un tournoi",
        "self.tournament_manager.run_tournament()"],
    0: [" 0 - Sortir de l'application", "self.quit()"]
}

DICT_ACTORS_MENU = {
    "titre": "Bienvenue dans le menu de gestion des joueurs",
    1: [" 1 - Ajouter un nouveau joueur",
        "self.actors_manager.create_actor(DICT_CREATE_PLAYER_MENU)"],
    2: [" 2 - Mettre à jour le classement d'un joueur",
        "self.actors_manager.update_rank_player()"],
    3: [" 3 - Afficher la liste de tous les joueurs",
        "self.actors_manager.list_actors()"],
    4: [" 4 - Afficher la liste des joueurs  d'un tournoi",
        "self.actors_manager.list_actors_in_tournament()"],
    0: [" 0 - Revenir au menu précedent", "setattr(self, 'dict_menu', DICT_START_MENU)"]
}

DICT_TOURNAMENT_MENU = {
    "titre": "Bienvenue dans le menu de gestion des tournois",
    1: [" 1 - Ajouter un nouveau tournoi",
        "self.tournament_manager.create_tournament(DICT_CREATE_TOURNAMENT_MENU)"],
    2: [" 2 - Afficher la liste de tous les tournois",
        "self.tournament_manager.list_tournaments()"],
    3: [" 3 - Afficher la liste de tous les tours d'un tournoi",
        "self.tournament_manager.list_round_in_tournament()"],
    4: [" 4 - Afficher la liste de tous les matchs d'un tournoi",
        "self.tournament_manager.list_matches_by_round_in_tournament()"],
    0: [" 0 - Revenir au menu précedent", "setattr(self, 'dict_menu', DICT_START_MENU)"]
}
