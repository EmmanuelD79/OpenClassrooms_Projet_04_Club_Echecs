from constants.error_msg import ERROR


class Command:

    def show_menu(self, dict_menu_to_show):
        print()
        print(dict_menu_to_show["titre"])
        print("=" * len(dict_menu_to_show["titre"]))
        for n_option in range(1, len(dict_menu_to_show) - 1):
            print(dict_menu_to_show[n_option][0])
        print(dict_menu_to_show[0][0])

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

    def ask_choice(self):
        choice = input("Quel est votre choix ? ")
        return choice

    def show_add_player_menu(self, increment):
        selected_player = input(f"Entrer l'id du joueur n°{increment} ?")
        return selected_player

    def prompt_validate_add_player(self, confirmation, max_players):
        increment, id_player, validate = confirmation
        if validate:
            print(f"Joueur n° {increment} est {id_player}")
        elif validate and increment == max_players:
            print(f"Joueur n° {increment} est {id_player}")
            print("tous les joueurs sont enregistrés dans le tournoi")
        else:
            self.prompt_error("PLAYER ON BASE")

    def prompt_error(self, type_error):
        print(ERROR[type_error])

    def show_update_score(self, players, attribut, msg):
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

    def show_score(self, player, score, increment):
        print(
            f"{increment} - {player.first_name} {player.last_name} ({player.rank}) "
            f"a obtenu {score[1]} point(s)")

    def show_stop_tournament(self):
        print("tous les tours ont été joués")
        print("le tournoi est terminé")
        response = "Voulez_vous terminer le tournoi O/N ?"
        return response

    def show_quit(self):
        print("Au revoir")


class Tournament_report:

    def show_list_tournament(self, name, site, id, start, stop_msg, control_time, description):
        print()
        print(f"Le tournoi {name} à {site}\n"
              f"son id est :  {id}\n"
              f"{start}\n"
              f"{stop_msg}\n"
              f"Le contrôle du temps est  {control_time}\n"
              f"Description: {description}"
              )
        print("=" * len(stop_msg))

    def show_list_round_in_tournament(self, round_id, msg_start, msg_stop):
        print()
        print(f"Le tour {round_id}\n"
              f"{msg_start}")
        print(msg_stop)
        print("=" * len(msg_stop))

    def show_list_matches_in_tournament(self, match_id, round_id, player_1, player_2, msg_score):
        print(f"Le match {match_id} du tour : {round_id}")
        print(f"Le joueur : {player_1} a joué contre le joueur : {player_2}")
        print(msg_score)
        print("=" * len(msg_score))
        print()

    def show_match_round(self, match=""):
        if match == "":
            print("\nVoici les matches pour le nouveau tour:")
        else:
            print(match)


class Actors_report:

    def show_list_actors(self, id, first_name, last_name, date_of_birth, sex, rank):
        print()
        print(f"{last_name} {first_name} (id: {id}) est classé(e) n° {rank}")
        msg = f"né(e) : {date_of_birth} de sexe : {sex}"
        print(msg)
        print("=" * len(msg))
