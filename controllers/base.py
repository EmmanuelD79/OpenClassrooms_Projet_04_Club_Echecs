from models.actors import Actor
from models.tournaments import Tournament
from models.rounds import Round

from helpers.function import validate_format

import constants.config as DEFAULT
import constants.menus as MENU
import constants.error_manage as ERROR


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
        self.tournament_manager = TournamentManager(self.view, self.tournament_report)
        self.actors_manager = ActorsManager(self.view, self.actors_report)
        self.dict_menu = MENU.START

    def run(self):
        '''manage the menu navigation'''
        self.validate = True
        while self.validate:
            self.view.display_menu(self.dict_menu)
            choice = Controller.ask_menu_choice(self.dict_menu, self.view)
            eval(self.dict_menu[choice][1])

    def quit(self):
        self.view.display_quit()
        self.validate = False

    @staticmethod
    def ask_tournament_id(dict_tournaments, view):
        '''Ask ID of the tournament wanted'''
        validate = False
        while not validate:
            attr_value = view.prompt_questions(MENU.RUN_TOURNAMENT["id"][0], "id")

            if attr_value in dict_tournaments:
                obj_tournament = dict_tournaments[attr_value]
                return obj_tournament
            elif attr_value == "":
                return None
            else:
                view.display_error(ERROR.TOURNAMENT_NONE)

    @staticmethod
    def ask_menu_choice(menu, view):
        '''Ask and check the menu choice'''
        option = len(menu) - 1
        regex = f"[0-{option}]" + "{1}$"
        validate = False
        while not validate:
            str_choice = view.prompt_choice()
            validate = validate_format(str_choice, regex)
        int_choice = int(str_choice)
        return int_choice


class TournamentManager:

    def __init__(self, view, report):
        self.dict_menu = ""
        self.view = view
        self.report = report
        self.dict_tournaments = Tournament.load_all()
        self.dict_actors = Actor.load_all()

    def run_tournament(self):
        '''Run the tournament and manage the round and matches'''
        self.obj_tournament = Controller.ask_tournament_id(self.dict_tournaments, self.view)
        if self.obj_tournament is not None:
            players_validate = self.add_player_in_tournament()
            if players_validate:
                validate_exist_round = self.check_round_n()
                self.update_score_last_round(validate_exist_round)
                round_n = len(self.obj_tournament.l_rounds)
                if 0 <= round_n < DEFAULT.NB_ROUND:
                    self.create_new_round(round_n)
                    self.rank_players()
                    self.resume_matches_in_new_round()

                else:
                    if self.obj_tournament.stop is None:
                        stop_validate = self.view.prompt_stop_tournament()
                        if stop_validate:
                            self.obj_tournament.stop_to_play()
                            self.rank_players()
                            self.obj_tournament.save_db()
                            self.dict_tournaments = Tournament.load_all()
                    else:
                        self.rank_players()

    def create_new_round(self, round_n):
        '''Create a new round in the tournament'''
        list_sort_players = self.obj_tournament.sort_players_by_points_and_rank()
        new_round = Round(self.obj_tournament.id, list_sort_players, round_n + 1)
        for match_index in range(DEFAULT.MIN_MATCHES, DEFAULT.MAX_MATCHES + 1):
            index_list_sort_players = 1
            couple_validate = False
            while not couple_validate:
                couple_players = new_round.pair_players(list_sort_players)
                couple_validate = self.validate_pair_players(couple_players,
                                                             self.obj_tournament.l_done_matches)
                if couple_validate:
                    self.obj_tournament.l_done_matches.append(couple_players)
                    new_round.create_match(couple_players, match_index)
                    list_sort_players.pop(list_sort_players.index(couple_players[0]))
                    list_sort_players.pop(list_sort_players.index(couple_players[1]))
                else:
                    list_sort_players = self.change_list_players(list_sort_players,
                                                                 index_list_sort_players)
                    index_list_sort_players += 1
        new_round.start_to_play()
        self.obj_tournament.add_round(new_round)
        self.obj_tournament.save_db()
        self.dict_tournaments = Tournament.load_all()

    def rank_players(self):
        '''Rank players in tournament'''
        rank = self.obj_tournament.sort_players_by_points_and_rank()
        self.view.display_score()
        index_player = 1
        for player_id in rank:
            player = self.dict_actors[player_id]
            score = self.obj_tournament.l_players_points[player_id]
            self.view.display_score(player_id, player, score, index_player)
            index_player += 1

    def update_score_last_round(self, validate_exist_round):
        '''Do the last round score update'''
        if validate_exist_round:
            last_round = self.obj_tournament.l_rounds[-1]
            if last_round.stop is None:
                msg = MENU.UPDATE_SCORE["confirmation"][0]
                format = MENU.UPDATE_SCORE["confirmation"][1]
                confirmation = False
                while not confirmation:
                    response = self.view.display_update_score([], "confirmation", msg, last_round.id)
                    confirmation = validate_format(response, format)
                    if confirmation is False:
                        self.view.display_error(ERROR.BAD_TYPO)
                if response == "O":
                    l_matches = []
                    matches = last_round.matches
                    for match in matches:
                        msg = MENU.UPDATE_SCORE["score"][0]
                        format = MENU.UPDATE_SCORE["score"][1]
                        valide_score = False
                        while not valide_score:
                            score = self.view.display_update_score(match.couple_id, "score", msg, last_round.id)
                            valide_score = validate_format(score, format)
                            if valide_score is False:
                                self.view.display_error(ERROR.BAD_TYPO)
                        match.assign_score(score)
                        l_matches.append(match)
                    last_round.update_matches(l_matches)
                    last_round.stop_to_play()
                    self.obj_tournament.set_points()
                    self.obj_tournament.save_db()
                    self.dict_tournaments = Tournament.load_all()

    def resume_matches_in_new_round(self):
        '''Resume matches of the new round in the tournament'''
        last_round = self.obj_tournament.l_rounds[-1]
        self.view.display_match_round()
        for match in last_round.matches:
            self.view.display_match_round(match)

    def check_round_n(self):
        '''Check the n° of the current round'''
        round_n = len(self.obj_tournament.l_rounds)
        validate_exist_round = False
        if 0 < round_n <= DEFAULT.NB_ROUND:
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
        try:
            list_players[1], list_players[increment + 1] = list_players[increment + 1],\
                                                           list_players[1]
            return list_players
        except IndexError:
            self.view.display_error(ERROR.LIST_PLAYERS)

    def add_player_in_tournament(self):
        '''Add players in current tournament if the list players don't exists'''
        self.dict_actors = Actor.load_all()
        if (len(self.obj_tournament.l_players_id) < DEFAULT.MAX_PLAYERS) and \
                (len(self.dict_actors) >= DEFAULT.MAX_PLAYERS):
            lst_players = []
            score = {}
            for index_player in range(DEFAULT.MIN_PLAYERS, DEFAULT.MAX_PLAYERS + 1):
                while True:
                    selected_player = self.view.prompt_add_player_menu(index_player)
                    if (selected_player in self.dict_actors) \
                            and not (selected_player in lst_players):
                        lst_players.append(selected_player)
                        obj_player = self.dict_actors[selected_player]
                        score[selected_player] = [obj_player.rank, DEFAULT.SCORE]
                        self.view.prompt_validate_add_player(index_player, selected_player, DEFAULT.MAX_PLAYERS)
                        break
                    elif selected_player in lst_players:
                        self.view.display_error(ERROR.PLAYER_EXIST_IN_TOURNAMENT)
                    else:
                        self.view.display_error(ERROR.PLAYER_NONE)
            self.obj_tournament.add_players(lst_players, score)
            self.obj_tournament.start_to_play()
            self.obj_tournament.save_db()
            self.dict_tournaments = Tournament.load_all()
            players_validate = True

        elif len(self.obj_tournament.l_players_id) == DEFAULT.MAX_PLAYERS:
            players_validate = True
        else:
            self.view.display_error(ERROR.PLAYERS_NOT_ENOUGH)
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
                    if tournament_validate is False:
                        self.view.display_error(ERROR.BAD_TYPO)
                    if (attribut == "id") and (tournament_validate is True):
                        if response in self.dict_tournaments:
                            tournament_validate = False
                            self.view.display_error(ERROR.TOURNAMENT_EXIST)
                if attribut == "control_time":
                    response = CONTROL_TIME[response]
                setattr(tournament, attribut, response)
        tournament.save_db()
        self.dict_tournaments = Tournament.load_all()

    def list_tournaments(self):
        '''manage the list of all tournaments'''
        for tournament_item in self.dict_tournaments:
            obj_tournament = self.dict_tournaments[tournament_item]
            self.report.display_list_tournament(
                obj_tournament.name,
                obj_tournament.site,
                obj_tournament.id,
                obj_tournament.start,
                obj_tournament.stop,
                obj_tournament.control_time,
                obj_tournament.description
            )

    def list_round_in_tournament(self):
        '''Manage the list of round for one tournament'''
        self.obj_tournament = Controller.ask_tournament_id(self.dict_tournaments, self.view)
        if self.obj_tournament is not None:
            obj_rounds = self.obj_tournament.l_rounds
            for obj_round in obj_rounds:
                self.report.display_list_round_in_tournament(obj_round.id,
                                                             obj_round.start,
                                                             obj_round.stop)

    def list_matches_by_round_in_tournament(self):
        '''Manage the list of matches for one tournament'''
        self.obj_tournament = Controller.ask_tournament_id(self.dict_tournaments, self.view)
        if self.obj_tournament is not None:
            obj_rounds = self.obj_tournament.l_rounds
            for obj_round in obj_rounds:
                for obj_match in obj_round.matches:
                    player_1 = obj_match.score[0][0]
                    player_2 = obj_match.score[1][0]
                    score_player_1 = obj_match.score[0][1]
                    score_player_2 = obj_match.score[1][1]
                    self.report.display_list_matches_in_tournament(
                        obj_match.match_index,
                        obj_match.round_id,
                        player_1,
                        player_2,
                        score_player_1,
                        score_player_2
                    )


class ActorsManager:

    def __init__(self, view, actors_report):

        self.report = actors_report
        self.view = view
        self.dict_menu = ""
        self.dict_actors = Actor.load_all()
        self.dict_tournament = Tournament.load_all()

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
                if actors_validate is False:
                    self.view.display_error(ERROR.BAD_TYPO)
                if (attribut == "id") and (actors_validate is True):
                    if attr_value in self.dict_actors:
                        actors_validate = False
                        self.view.display_error(ERROR.PLAYER_EXIST)
            if attribut == "rank":
                attr_value = int(attr_value)
            setattr(actor, attribut, attr_value)
        actor.save_db()
        self.dict_actors = Actor.load_all()

    def list_actors(self):
        '''Manage the list of all actors'''
        lst_actors = self.get_list_actors()
        self.sort_list_actors(lst_actors)

    def list_actors_in_tournament(self):
        '''Manage the list of all actors in one tournament'''
        self.dict_tournament = Tournament.load_all()
        obj_tournament = Controller.ask_tournament_id(self.dict_tournament, self.view)
        lst_actors = self.get_list_actors(obj_tournament)
        self.sort_list_actors(lst_actors)

    def get_list_actors(self, obj_tournament=None):
        '''Get the list of all actors or players in one tournament'''
        l_actors = []
        l_id_actors = self.dict_actors.keys()
        if obj_tournament is not None:
            l_id_actors = obj_tournament.l_players_id
        for id_actor in l_id_actors:
            obj_actor = self.dict_actors[id_actor]
            l_actor_info = [
                id_actor,
                obj_actor.first_name,
                obj_actor.last_name,
                obj_actor.date_of_birth,
                obj_actor.sex,
                obj_actor.rank
            ]
            l_actors.append(l_actor_info)
        return l_actors

    def sort_list_actors(self, lst_actors):
        '''Sort the list actors by last_name or by Rank'''
        self.view.display_menu(MENU.SORT)
        choice = Controller.ask_menu_choice(MENU.SORT, self.view)
        if choice == 1:
            index = INDEX_LAST_NAME
        elif choice == 2:
            index = INDEX_RANK
        for actor in sorted(lst_actors, key=lambda actor_sort: actor_sort[index]):
            obj_actor = self.dict_actors[actor[0]]
            self.report.display_list_actors(
                obj_actor.id,
                obj_actor.first_name,
                obj_actor.last_name,
                obj_actor.date_of_birth,
                obj_actor.sex,
                obj_actor.rank
            )

    def update_rank_player(self):
        '''Do the rank of one player update'''
        if self.dict_actors != {}:
            for key_menu in MENU.UPDATE_RANK:
                if key_menu == "titre":
                    self.view.prompt_questions(MENU.UPDATE_RANK["titre"][0], "titre")
                elif key_menu == "id":
                    msg = MENU.UPDATE_RANK[key_menu][0]
                    id_validate = False
                    while not id_validate:
                        response = self.view.prompt_questions(msg, key_menu)
                        if response in self.dict_actors:
                            obj_actor = self.dict_actors[response]
                            id_validate = True
                        else:
                            id_validate = False
                elif key_menu == "rank":
                    msg = MENU.UPDATE_RANK[key_menu][0] % (obj_actor.first_name, obj_actor.last_name, obj_actor.rank)
                    valide_format = MENU.UPDATE_RANK[key_menu][1]
                    rank_validate = False
                    while not rank_validate:
                        new_rank = self.view.prompt_questions(msg, key_menu)
                        rank_validate = validate_format(new_rank, valide_format)
                elif key_menu == "confirmation":
                    msg = MENU.UPDATE_RANK[key_menu][0] % (obj_actor.rank, new_rank)
                    valide_format = MENU.UPDATE_RANK[key_menu][1]
                    new_rank_validate = False
                    while not new_rank_validate:
                        response = self.view.prompt_questions(msg, key_menu)
                        new_rank_validate = validate_format(response, valide_format)
                        if response == "O":
                            obj_actor.update_rank(int(new_rank))
                            obj_actor.save_db()
                            self.dict_actors = Actor.load_all()
                            msg = MENU.UPDATE_RANK["save"][0] % (obj_actor.first_name,
                                                                 obj_actor.last_name,
                                                                 new_rank)
                            self.view.prompt_questions(msg, "save")
        else:
            self.view.display_error(ERROR.NO_PLAYERS)
