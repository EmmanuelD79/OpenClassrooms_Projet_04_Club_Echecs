class CommandView:

    def display_menu(self, dict_menu_to_show):
        print()
        print(dict_menu_to_show["titre"])
        print("=" * len(dict_menu_to_show["titre"]))
        for n_option in range(1, len(dict_menu_to_show) - 1):
            print(dict_menu_to_show[n_option][0])
        print(dict_menu_to_show[0][0])

    def display_match_round(self, match=""):
        if match == "":
            print("\nVoici les matches pour le nouveau tour:")
        else:
            print(match)

    def display_update_score(self, players, attribut, msg):
        if attribut == "confirmation":
            print("Le dernier round n'est pas fini")
            print(
                "Vous devez mettre à jour les scores pour ce round"
            )
            response = input(msg)
        else:
            print(
                f" Joueur : {players[0]} "
                "contre Joueur : "
                f"{players[1]}"
            )
            response = input(msg)
        return response

    def display_score(self, player, score, index_player):
        print(
            f"{index_player} - {player.first_name} {player.last_name} ({player.rank}) "
            f"a obtenu {score[1]} point(s)")

    def display_error(self, type_error):
        print(type_error)

    def display_quit(self):
        print("Au revoir")

    def prompt_questions(self, msg, attribut):
        if attribut == "titre":
            print(msg)
            print("=" * len(msg))
            response = None
        elif attribut == "save":
            print(msg)
            response = None
        else:
            response = input(msg)
        return response

    def prompt_choice(self):
        choice = input("Quel est votre choix ? ")
        return choice

    def prompt_add_player_menu(self, index_player):
        selected_player = input(f"Entrer l'id du joueur n°{index_player} ?")
        return selected_player

    def prompt_validate_add_player(self, index_player, id_player, max_players):
        print(f"Joueur n° {index_player} est {id_player}")
        if index_player == max_players:
            print("tous les joueurs sont enregistrés dans le tournoi")

    def prompt_stop_tournament(self):
        print("tous les tours ont été joués")
        print("le tournoi est terminé")
        response = "Voulez_vous terminer le tournoi O/N ?"
        return response


class TournamentReport:

    def display_list_tournament(self, name, site, id, start, stop, control_time, description):
        if start is None:
            start_msg = "Actuellement, il n'a pas commencé"
        else:
            start_msg = f"Il a commencé {start}"
        if stop is None:
            stop_msg = "Actuellement, il n'est pas terminé"
        else:
            stop_msg = f"Il s'est terminé {stop}"
        print()
        print(f"Le tournoi {name} à {site}\n"
              f"son id est :  {id}\n"
              f"{start_msg}\n"
              f"{stop_msg}\n"
              f"Le contrôle du temps est  {control_time}\n"
              f"Description: {description}"
              )
        print("=" * len(stop_msg))

    def display_list_round_in_tournament(self, round_id, round_start, round_stop):
        if round_start is None:
            msg_start = "Le round n'a pas débuté"
        else:
            msg_start = f"le round a débuté {round_start}"
        if round_stop is None:
            msg_stop = "Le round n'est pas terminé"
        else:
            msg_stop = f"le round s'est terminé {round_stop}"
        print()
        print(f"Le tour {round_id}\n"
              f"{msg_start}")
        print(msg_stop)
        print("=" * len(msg_stop))

    def display_list_matches_in_tournament(
            self,
            match_id,
            round_id,
            player_1,
            player_2,
            score_player_1,
            score_player_2
    ):

        if score_player_1 == 1:
            msg_score = f"Le joueur : {player_1} est le vainqueur du match"
        elif score_player_2 == 1:
            msg_score = f"Le joueur : {player_2} est le vainqueur du match"
        elif (score_player_1 == 0) and (score_player_2 == 0):
            msg_score = "Le match n'a pas encore été joué"
        else:
            msg_score = "Les joueurs ont fait match nul"
        print(f"Le match {match_id} du tour : {round_id}")
        print(f"Le joueur : {player_1} a joué contre le joueur : {player_2}")
        print(msg_score)
        print("=" * len(msg_score))
        print()


class ActorsReport:

    def display_list_actors(self, id, first_name, last_name, date_of_birth, sex, rank):
        print()
        print(f"{last_name} {first_name} (id: {id}) est classé(e) n° {rank}")
        msg = f"né(e) : {date_of_birth} de sexe : {sex}"
        print(msg)
        print("=" * len(msg))
