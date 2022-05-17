from models.actors import Actor
from models.tournaments import Tournament
from models.rounds import Round
from constants.menus import DICT_START_MENU,\
    DICT_TOURNAMENT_MENU, DICT_ACTORS_MENU, DICT_CREATE_TOURNAMENT_MENU, DICT_CREATE_PLAYER_MENU,\
    DICT_SORT, DICT_UPDATE_RANK, DICT_RUN_TOURNAMENT
from helpers.function import validate_format
from constants.base import MAX_PLAYERS, MAX_MATCHES, MIN_PLAYERS, MIN_MATCHES, DEFAULT_SCORE, DEFAULT_NB_ROUND


# index de l'attribut last_name dans l'objet Actor
INDEX_LAST_NAME = 2

# index de l'attribut rank dans l'objet Actor
INDEX_RANK = 5

# Dictionnaire des differents modes de control time
CONTROL_TIME = {"1": "Bullet", "2": "Blizt", "3": "Coup rapide"}


class Controller:

    def __init__(self, view, actors_report, tournament_report):

        self.dict_actors = Actor().load_all()
        self.dict_tournaments = Tournament().load_all()
        self.view = view
        self.actors_report = actors_report
        self.tournament_report = tournament_report
        self.tournament_manager = TournamentManager(self.view, self.
                                                    tournament_report, self.dict_tournaments, self.dict_actors)
        self.actors_manager = ActorsManager(self.view,
                                            self.actors_report, self.dict_tournaments, self.dict_actors)
        self.dict_menu = DICT_START_MENU

    def run(self):
        '''manage the menu navigation'''
        self.validate = True
        while self.validate:
            self.view.show_menu(self.dict_menu)
            choice = Controller.ask_menu_choice(self.dict_menu, self.view)
            eval(self.dict_menu[choice][1])

    def quit(self):
        self.view.show_quit()
        self.validate = False

    @staticmethod
    def ask_tournament_id(dict_tournaments, view):
        '''Ask ID of the tournament wanted'''
        validate = False
        while not validate:
            attr_value = view.prompt_questions(DICT_RUN_TOURNAMENT["id"][0], "id")
            validate = False
            if attr_value in dict_tournaments:
                obj_tournament = dict_tournaments[attr_value]
                return obj_tournament

    @staticmethod
    def ask_menu_choice(menu, view):
        '''Ask and check the menu choice'''
        option = len(menu) - 1
        regex = f"[0-{option}]" + "{1}$"
        validate = False
        while not validate:
            choice = view.ask_choice()
            validate = validate_format(choice, regex)
        choice = int(choice)
        return choice


class TournamentManager:

    def __init__(self, view, report, dict_tournament, dict_actors):
        self.dict_menu = ""
        self.view = view
        self.report = report
        self.dict_tournaments = dict_tournament
        self.dict_actors = dict_actors

    def run_tournament(self):
        '''Run the tournament and manage the round and matches'''
        self.obj_tournament = Controller.ask_tournament_id(self.dict_tournaments, self.view)
        players_validate = self.add_player_in_tournament()
        if players_validate:
            validate_exist_round = self.check_round_n()
            self.update_score_last_round(validate_exist_round)
            round_n = len(self.obj_tournament.l_rounds)
            if 0 <= round_n < DEFAULT_NB_ROUND:
                self.create_new_round(round_n)
                self.resume_matches_in_new_round()
            else:
                if self.obj_tournament.stop is None:
                    stop_validate = self.view.show_stop_tournament()
                    if stop_validate:
                        self.obj_tournament.stop_to_play()
                        self.rank_players()
                        self.obj_tournament.save_db()
                        self.dict_tournaments = self.obj_tournament.load_all()
                else:
                    self.rank_players()

    def create_new_round(self, round_n):
        '''Create a new round in the tournament'''
        list_sort_players = self.obj_tournament.sort_players_by_points_and_rank()
        new_round = Round(self.obj_tournament.id, list_sort_players, round_n + 1)
        for match_index in range(MIN_MATCHES, MAX_MATCHES + 1):
            increment = 1
            couple_validate = False
            while not couple_validate:
                couple_players = new_round.pair_players(list_sort_players)
                couple_validate = self.validate_pair_players(couple_players, self.obj_tournament.l_done_matches)
                if couple_validate:
                    self.obj_tournament.l_done_matches.append(couple_players)
                    new_round.create_match(couple_players, match_index)
                    list_sort_players.pop(list_sort_players.index(couple_players[0]))
                    list_sort_players.pop(list_sort_players.index(couple_players[1]))
                else:
                    list_sort_players = self.change_list_players(list_sort_players, increment)
                    increment += 1
        new_round.start_to_play()
        self.obj_tournament.add_round(new_round)
        self.obj_tournament.save_db()
        self.dict_tournaments = self.obj_tournament.load_all()

    def rank_players(self):
        '''Rank players in tournament'''
        rank = self.obj_tournament.sort_players_by_points_and_rank()
        increment = 1
        for player_id in rank:
            player = self.dict_actors[player_id]
            score = self.obj_tournament.l_players_points[player_id]
            self.view.show_score(player, score, increment)
            increment += 1

    def update_score_last_round(self, validate_exist_round):
        '''Do the last round score update'''
        if validate_exist_round:
            last_round = self.obj_tournament.l_rounds[-1]
            if last_round.stop is None:
                response = self.view.show_update_score([], False)
                if response == "O":
                    l_matches = []
                    matches = last_round.matches
                    for match in matches:
                        score = self.view.show_update_score(match.couple_id, True)
                        match.assign_score(score)
                        l_matches.append(match)
                    last_round.update_matches(l_matches)
                    last_round.stop_to_play()
                    self.obj_tournament.set_points()
                    self.obj_tournament.save_db()
                    self.dict_tournaments = self.obj_tournament.load_all()

    def resume_matches_in_new_round(self):
        '''Resume matches of the new round in the tournament'''
        last_round = self.obj_tournament.l_rounds[-1]
        for match in last_round.matches:
            self.report.show_match_round(match)

    def check_round_n(self):
        '''Check the n° of the current round'''
        round_n = len(self.obj_tournament.l_rounds)
        validate_exist_round = False
        if 0 < round_n <= DEFAULT_NB_ROUND:
            validate_exist_round = True
        return validate_exist_round

    def validate_pair_players(self, pair, already_done_matches):
        '''Valide if couple players already don't exists'''
        pair_reverse = [pair[1], pair[0]]
        pair_validate = True
        if (pair in already_done_matches) or (pair_reverse in already_done_matches):
            pair_validate = False
        return pair_validate

    def change_list_players(self, list_players, increment):
        '''Take the next player, if the couple players already exists'''
        list_players[1], list_players[increment + 1] = list_players[increment + 1], list_players[1]
        return list_players

    def add_player_in_tournament(self):
        '''Add players in current tournament if the list players don't exists'''
        if (len(self.obj_tournament.l_players_id) < MAX_PLAYERS) and \
                (len(self.dict_actors) >= MAX_PLAYERS):
            lst_players = []
            score = {}
            for increment in range(MIN_PLAYERS, MAX_PLAYERS + 1):
                while True:
                    selected_player = self.view.show_add_player_menu(increment)
                    if (selected_player in self.dict_actors) \
                            and not (selected_player in lst_players):
                        lst_players.append(selected_player)
                        obj_player = self.dict_actors[selected_player]
                        score[selected_player] = [obj_player.rank, DEFAULT_SCORE]
                        confirmation = [increment, selected_player, True]
                        self.view.prompt_validate_add_player(confirmation, MAX_PLAYERS)
                        break
                    else:
                        confirmation = [increment, selected_player, False]
                        self.view.prompt_validate_add_player(confirmation, MAX_PLAYERS)
            self.obj_tournament.add_players(lst_players, score)
            self.obj_tournament.start_to_play()
            self.obj_tournament.save_db()
            self.dict_tournaments = self.obj_tournament.load_all()
            players_validate = True

        elif len(self.obj_tournament.l_players_id) == MAX_PLAYERS:
            players_validate = True
        else:
            self.view.prompt_error()
            players_validate = False

        return players_validate

    def create_tournament(self, dict_menu):
        '''Create a new tournament'''
        self.dict_menu = dict_menu
        self.view.prompt_questions(self.dict_menu["titre"][0], "titre")
        tournament = Tournament()
        lst_attribut = tournament.attribut_getter()
        for attribut in lst_attribut:
            if attribut in self.dict_menu:
                msg = self.dict_menu[attribut][0]
                valide_format = self.dict_menu[attribut][1]
                tournament_validate = False
                while not tournament_validate:
                    response = self.view.prompt_questions(msg, attribut)
                    tournament_validate = validate_format(response, valide_format)
                if attribut == "control_time":
                    response = CONTROL_TIME[response]
                setattr(tournament, attribut, response)
        tournament.save_db()
        self.dict_tournaments = tournament.load_all()

    def list_tournaments(self):
        '''manage the list of all tournaments'''
        for tournament_item in self.dict_tournaments:
            obj_tournament = self.dict_tournaments[tournament_item]
            if obj_tournament.start is None:
                start_msg = "Actuellement, il n'a pas commencé"
            else:
                start_msg = f"Il a commencé {obj_tournament.start}"

            if obj_tournament.stop is None:
                stop_msg = "Actuellement, il n'est pas terminé"
            else:
                stop_msg = f"Il s'est terminé {obj_tournament.stop}"
            self.report.show_list_tournament(obj_tournament.name,
                                             obj_tournament.site,
                                             obj_tournament.id,
                                             start_msg,
                                             stop_msg,
                                             obj_tournament.control_time,
                                             obj_tournament.description
                                             )

    def list_round_in_tournament(self):
        '''Manage the list of round for one tournament'''
        self.obj_tournament = Controller.ask_tournament_id(self.dict_tournaments, self.view)
        obj_rounds = self.obj_tournament.l_rounds
        for obj_round in obj_rounds:
            if obj_round.start is None:
                msg_start = "Le round n'a pas débuté"
            else:
                msg_start = f"le round a débuté {obj_round.start}"
            if obj_round.stop is None:
                msg_stop = "Le round n'est pas terminé"
            else:
                msg_stop = f"le round s'est terminé {obj_round.stop}"
            self.report.show_list_round_in_tournament(obj_round.id, msg_start, msg_stop)

    def list_matches_by_round_in_tournament(self):
        '''Manage the list of matches for one tournament'''
        self.obj_tournament = Controller.ask_tournament_id(self.dict_tournaments, self.view)
        obj_rounds = self.obj_tournament.l_rounds
        for obj_round in obj_rounds:
            for obj_match in obj_round.matches:
                if obj_match.score[0][1] == 1:
                    msg_score = f"Le joueur : {obj_match.score[0][0]} est le vainqueur du match"
                elif obj_match.score[1][1] == 1:
                    msg_score = f"Le joueur : {obj_match.score[1][0]} est le vainqueur du match"
                elif (obj_match.score[0][1] == 0) and (obj_match.score[1][1] == 0):
                    msg_score = "Le match n'a pas encore été joué"
                else:
                    msg_score = "Les joueurs ont fait match nul"
                self.report.show_list_matches_in_tournament(obj_match.match_index,
                                                            obj_match.round_id,
                                                            obj_match.score[0][0],
                                                            obj_match.score[1][0],
                                                            msg_score
                                                            )


class ActorsManager:

    def __init__(self, view, actors_report, dict_tournament, dict_actors):

        self.report = actors_report
        self.view = view
        self.dict_menu = ""
        self.dict_actors = dict_actors
        self.dict_tournament = dict_tournament

    def create_actor(self, dict_menu):
        '''Create a new actor'''
        self.dict_menu = dict_menu
        self.view.prompt_questions(self.dict_menu["titre"], "titre")
        actor = Actor()
        lst_attribut = actor.attribut_getter()
        for attribut in lst_attribut:
            msg = self.dict_menu[attribut][0]
            valide_format = self.dict_menu[attribut][1]
            actors_validate = False
            while not actors_validate:
                attr_value = self.view.prompt_questions(msg, attribut)
                actors_validate = validate_format(attr_value, valide_format)
            if attribut == "rank":
                attr_value = int(attr_value)
            setattr(actor, attribut, attr_value)
        actor.save_db()
        self.dict_actors = actor.load_all()

    def list_actors(self):
        '''Manage the list of all actors'''
        lst_actors = self.get_list_actors()
        self.sort_list_actors(lst_actors)

    def list_actors_in_tournament(self):
        '''Manage the list of all actors in one tournament'''
        obj_tournament = Controller.ask_tournament_id(self.dict_tournament, self.view)
        lst_actors = self.get_list_actors(obj_tournament)
        self.sort_list_actors(lst_actors)

    def get_list_actors(self, obj_tournament=None):
        '''Get the list of all actors or players in one tournament'''
        source_actor_list = self.dict_actors
        if obj_tournament is not None:
            source_actor_list = obj_tournament.l_players_id
        lst_actors = []
        for id_actor in source_actor_list:
            obj_actor = self.dict_actors[id_actor]
            lst_actor = [
                id_actor,
                obj_actor.first_name,
                obj_actor.last_name,
                obj_actor.date_of_birth,
                obj_actor.sex,
                obj_actor.rank
            ]
            lst_actors.append(lst_actor)
        return lst_actors

    def sort_list_actors(self, lst_actors):
        '''Sort the list actors by last_name or by Rank'''
        self.view.show_menu(DICT_SORT)
        choice = Controller.ask_menu_choice(DICT_SORT, self.view)
        if choice == 1:
            index = INDEX_LAST_NAME
        elif choice == 2:
            index = INDEX_RANK
        for actor in sorted(lst_actors, key=lambda actor_sort: actor_sort[index]):
            obj_actor = self.dict_actors[actor[0]]
            self.report.show_list_actors(obj_actor.id,
                                         obj_actor.first_name,
                                         obj_actor.last_name,
                                         obj_actor.date_of_birth,
                                         obj_actor.sex,
                                         obj_actor.rank)

    def update_rank_player(self):
        '''Do the rank of one player update'''
        for key in DICT_UPDATE_RANK:
            if key == "titre":
                self.view.prompt_questions(DICT_UPDATE_RANK["titre"][0], "titre")
            elif key == "id":
                msg = DICT_UPDATE_RANK[key][0]
                id_validate = False
                while not id_validate:
                    response = self.view.prompt_questions(msg, key)
                    if response in self.dict_actors:
                        obj_actor = self.dict_actors[response]
                        id_validate = True
                    else:
                        id_validate = False
            elif key == "rank":
                msg = DICT_UPDATE_RANK[key][0] % (obj_actor.first_name, obj_actor.last_name, obj_actor.rank)
                valide_format = DICT_UPDATE_RANK[key][1]
                rank_validate = False
                while not rank_validate:
                    new_rank = self.view.prompt_questions(msg, key)
                    rank_validate = validate_format(new_rank, valide_format)
            elif key == "confirmation":
                msg = DICT_UPDATE_RANK[key][0] % (obj_actor.rank, new_rank)
                valide_format = DICT_UPDATE_RANK[key][1]
                new_rank_validate = False
                while not new_rank_validate:
                    response = self.view.prompt_questions(msg, key)
                    new_rank_validate = validate_format(response, valide_format)
                    if response == "O":
                        obj_actor.update_rank(int(new_rank))
                        obj_actor.save_db()
                        self.dict_actors = obj_actor.load_all()
                        msg = DICT_UPDATE_RANK["save"][0] % (obj_actor.first_name,
                                                             obj_actor.last_name,
                                                             new_rank)
                        self.view.prompt_questions(msg, "save")
