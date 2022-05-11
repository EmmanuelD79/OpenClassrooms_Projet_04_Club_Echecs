from models.actors import Actor
from models.tournaments import Tournament
from models.rounds import Round
from constants.menus import DICT_START_MENU,\
    DICT_TOURNAMENT_MENU, DICT_ACTORS_MENU, DICT_CREATE_TOURNAMENT_MENU, DICT_CREATE_PLAYER_MENU,\
    DICT_SORT, DICT_UPDATE_RANK, DICT_RUN_TOURNAMENT
from views.base import Command, Tournament_report, Actors_report
from helpers.function import validate_format
from constants.base import MAX_PLAYERS, MAX_MATCHES, MIN_PLAYERS, MIN_MATCHES, DEFAULT_SCORE, DEFAULT_NB_ROUND

# index de l'attribut last_name dans l'objet Actor
INDEX_LAST_NAME = 2

# index de l'attribut rank dans l'objet Actor
INDEX_RANK = 5

# Dictionnaire des differents modes de control time
CONTROL_TIME = {"1": "Bullet", "2": "Blizt", "3": "Coup rapide"}


class Controller:

    def __init__(self):

        self.dict_actors = Actor().load_all()
        self.dict_tournaments = Tournament().load_all()

    def run(self):

        self.menu = Menu(DICT_START_MENU)


class Menu:

    def __init__(self, dict_menu):
        self.view = Command()
        self.menu = dict_menu
        self.next_menu = eval(self.run())

    def run(self):
        self.view.show_menu(self.menu)
        option = len(self.menu) - 1
        regex = f"[0-{option}]" + "{1}$"
        validate = False
        while not validate:
            choice = self.view.ask_choice()
            validate = validate_format(choice, regex)
        choice = int(choice)
        return self.menu[choice][1]

    def stop(self):
        self.view.show_quit()


class TournamentManager():

    def __init__(self, dict_menu):
        self.view = Command()
        self.menu = dict_menu
        self.report = Tournament_report()
        self.control = Controller()
        self.dict_tournaments = self.control.dict_tournaments
        self.dict_actors = self.control.dict_actors

    def run_tournament(self):
        self.obj_tournament = self.ask_tournament_id()
        validate = self.add_player_in_tournament()
        if validate:
            validate_exist_round = self.check_round_n()
            self.update_score_last_round(validate_exist_round)
            round_n = len(self.obj_tournament.l_rounds)
            if 0 <= round_n < DEFAULT_NB_ROUND:
                self.create_new_round(round_n)
                self.resume_matches_in_new_round()
            else:
                if self.obj_tournament.stop is None:
                    validate = self.view.show_stop_tournament()
                    if validate:
                        self.obj_tournament.stop_to_play()
                        self.rank_players()
                        self.obj_tournament.save_me()
                        self.dict_tournaments = self.obj_tournament.load_all()
                else:
                    self.rank_players()
        Menu(DICT_TOURNAMENT_MENU)

    def create_new_round(self, round_n):
        new_round = Round()
        new_round.create_me(self.obj_tournament.id, round_n + 1)
        list_sort_players = self.obj_tournament.sort_players_by_points_and_rank()
        setattr(new_round, "l_players_id", list_sort_players)
        for match_index in range(MIN_MATCHES, MAX_MATCHES + 1):
            increment = 1
            validate = False
            while not validate:
                couple_players = new_round.pair_players(list_sort_players)
                validate = self.validate_pair_players(couple_players, self.obj_tournament.l_done_matches)
                if validate:
                    self.obj_tournament.l_done_matches.append(couple_players)
                    new_round.create_match(couple_players, match_index)
                    list_sort_players.pop(list_sort_players.index(couple_players[0]))
                    list_sort_players.pop(list_sort_players.index(couple_players[1]))
                else:
                    list_sort_players = self.change_list_players(list_sort_players, increment)
                    increment += 1
        new_round.start_to_play()
        self.obj_tournament.add_round(new_round)
        self.obj_tournament.save_me()
        self.dict_tournaments = self.obj_tournament.load_all()

    def rank_players(self):
        rank = self.obj_tournament.sort_players_by_points_and_rank()
        increment = 1
        for player_id in rank:
            player = self.dict_actors[player_id]
            score = self.obj_tournament.l_players_points[player_id]
            self.view.show_score(player, score, increment)
            increment += 1

    def update_score_last_round(self, validate_exist_round):
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
                    last_round.add_matches(l_matches)
                    last_round.stop_to_play()
                    self.obj_tournament.set_points()
                    self.obj_tournament.save_me()
                    self.dict_tournaments = self.obj_tournament.load_all()

    def resume_matches_in_new_round(self):
        last_round = self.obj_tournament.l_rounds[-1]
        for match in last_round.matches:
            self.report.show_match_round(match)

    def change_list_players(self, list_players, increment):
        list_players[1], list_players[increment + 1] = list_players[increment + 1], list_players[1]
        return list_players

    def ask_tournament_id(self):
        validate = False
        while not validate:
            attr_value = self.view.prompt_questions(DICT_RUN_TOURNAMENT["id"][0], "id")
            valide_format = DICT_RUN_TOURNAMENT["id"][1]
            validate = validate_format(attr_value, valide_format)
            if validate:
                if attr_value in self.dict_tournaments:
                    obj_tournament = self.dict_tournaments[attr_value]
                    return obj_tournament
                else:
                    validate = False

    def check_round_n(self):
        round_n = len(self.obj_tournament.l_rounds)
        if 0 < round_n <= DEFAULT_NB_ROUND:
            validate_exist_round = True
        else:
            validate_exist_round = False
        return validate_exist_round

    def validate_pair_players(self, pair, already_done_matches):
        pair_reverse = [pair[1], pair[0]]
        if (pair in already_done_matches) or (pair_reverse in already_done_matches):
            validate = False
        else:
            validate = True
        return validate

    def add_player_in_tournament(self):
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
                        self.view.prompt_validate_add_player(confirmation)
                        break
                    else:
                        confirmation = [increment, selected_player, False]
                        self.view.prompt_validate_add_player(confirmation)
                setattr(self.obj_tournament, "l_players_id", lst_players)
                setattr(self.obj_tournament, "l_players_points", score)
            self.obj_tournament.start_to_play()
            self.obj_tournament.save_me()
            self.dict_tournaments = self.obj_tournament.load_all()

            validate = True
        elif len(self.obj_tournament.l_players_id) == MAX_PLAYERS:
            validate = True
        else:
            self.view.prompt_error()
            validate = False
        return validate

    def create_tournament(self):
        self.view.prompt_questions(self.menu["titre"][0], "titre")
        tournament = Tournament()
        lst_attribut = [
            attr for attr in tournament.__dict__
            if not callable(getattr(tournament, attr)) and not attr.startswith("_")
        ]

        for attribut in lst_attribut:
            if attribut in self.menu:
                msg = self.menu[attribut][0]
                valide_format = self.menu[attribut][1]
                validate = False
                while not validate:
                    attr_value = self.view.prompt_questions(msg, attribut)
                    validate = validate_format(attr_value, valide_format)
                if attribut == "control_time":
                    attr_value = CONTROL_TIME[attr_value]
                setattr(tournament, attribut, attr_value)
        tournament.save_me()
        self.dict_tournaments = tournament.load_all()
        Menu(DICT_TOURNAMENT_MENU)

    def list_tournaments(self):
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
        Menu(DICT_TOURNAMENT_MENU)

    def list_round_in_tournament(self):
        obj_tournament = self.ask_tournament_id()
        obj_rounds = obj_tournament.l_rounds
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
        Menu(DICT_TOURNAMENT_MENU)

    def show_list_matches_by_round_in_tournament(self):
        obj_tournament = self.ask_tournament_id()
        obj_rounds = obj_tournament.l_rounds
        for obj_round in obj_rounds:
            for obj_match in obj_round.matches:
                if obj_match.match[0][1] == 1:
                    msg_score = f"Le joueur : {obj_match.match[0][0]} est le vainqueur du match"
                elif obj_match.match[1][1] == 1:
                    msg_score = f"Le joueur : {obj_match.match[0][0]} est le vainqueur du match"
                elif (obj_match.match[0][1] == 0) and (obj_match.match[1][1] == 0):
                    msg_score = "Le match n'a pas encore été joué"
                else:
                    msg_score = "Les joueurs ont fait match nul"
                self.report.show_list_matches_in_tournament(obj_match.match_index,
                                                            obj_match.round_id,
                                                            obj_match.match[0][0],
                                                            obj_match.match[1][0],
                                                            msg_score
                                                            )
        Menu(DICT_TOURNAMENT_MENU)


class ActorsManager():

    def __init__(self, dict_menu):
        self.view = Command()
        self.control = Controller()
        self.dict_actors = self.control.dict_actors
        self.dict_tournaments = self.control.dict_tournaments
        self.report = Actors_report()
        self.menu = dict_menu

    def create_actor(self):
        self.view.prompt_questions(self.menu["titre"], "titre")
        actor = Actor()
        lst_attribut = [attr for attr in actor.__dict__ if
                        not callable(getattr(actor, attr)) and not attr.startswith("_")]
        for attribut in lst_attribut:
            msg = self.menu[attribut][0]
            valide_format = self.menu[attribut][1]
            validate = False
            while not validate:
                attr_value = self.view.prompt_questions(msg, attribut)
                validate = validate_format(attr_value, valide_format)
            if attribut == "rank":
                attr_value = int(attr_value)
            setattr(actor, attribut, attr_value)
        actor.save_me()
        self.dict_actors = actor.load_all()
        Menu(DICT_ACTORS_MENU)

    def list_actors(self):
        lst_actors = []
        for id_actor in self.dict_actors:
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
        self.view.show_menu(DICT_SORT)
        option = len(self.menu) - 1
        regex = f"[0-{option}]" + "{1}$"
        validate = False
        while not validate:
            choice = self.view.ask_choice()
            validate = validate_format(choice, regex)
        choice = int(choice)
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
        Menu(DICT_ACTORS_MENU)

    def list_actors_in_tournament(self):
        obj_tournament = self.ask_tournament_id()
        lst_actors = []
        for id_actor in obj_tournament.l_players_id:
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
        self.view.show_menu(DICT_SORT)
        option = len(self.menu) - 1
        regex = f"[0-{option}]" + "{1}$"
        validate = False
        while not validate:
            choice = self.view.ask_choice()
            validate = validate_format(choice, regex)
        choice = int(choice)
        if choice == 1:
            index = INDEX_LAST_NAME
        elif choice == 2:
            index = INDEX_RANK
        for actor in sorted(lst_actors, key=lambda actor_sort: actor_sort[index]):
            obj_actor = self.dict_actors[actor[0]]
            self.report.show_list_actors(
                obj_actor.id,
                obj_actor.first_name,
                obj_actor.last_name,
                obj_actor.date_of_birth,
                obj_actor.sex,
                obj_actor.rank
            )
        Menu(DICT_ACTORS_MENU)

    def ask_tournament_id(self):
        validate = False
        while not validate:
            attr_value = self.view.prompt_questions(DICT_RUN_TOURNAMENT["id"][0], "id")
            valide_format = DICT_RUN_TOURNAMENT["id"][1]
            validate = validate_format(attr_value, valide_format)
            if attr_value in self.dict_tournaments:
                obj_tournament = self.dict_tournaments[attr_value]
                return obj_tournament
            else:
                validate = False

    def update_rank_player(self):
        for key in DICT_UPDATE_RANK:
            if key == "titre":
                self.view.prompt_questions(DICT_UPDATE_RANK["titre"][0], "titre")
            elif key == "id":
                msg = DICT_UPDATE_RANK[key][0]
                validate = False
                while not validate:
                    response = self.view.prompt_questions(msg, key)
                    if response in self.dict_actors:
                        obj_actor = self.dict_actors[response]
                        validate = True
                    else:
                        validate = False
            elif key == "rank":
                msg = DICT_UPDATE_RANK[key][0] % (obj_actor.first_name, obj_actor.last_name, obj_actor.rank)
                valide_format = DICT_UPDATE_RANK[key][1]
                validate = False
                while not validate:
                    new_rank = self.view.prompt_questions(msg, key)
                    validate = validate_format(new_rank, valide_format)
            elif key == "confirmation":
                msg = DICT_UPDATE_RANK[key][0] % (obj_actor.rank, new_rank)
                valide_format = DICT_UPDATE_RANK[key][1]
                validate = False
                while not validate:
                    response = self.view.prompt_questions(msg, key)
                    validate = validate_format(response, valide_format)
                    if response == "O":
                        obj_actor.update_rank(int(new_rank))
                        obj_actor.save_me()
                        self.dict_actors = obj_actor.load_all()
                        msg = DICT_UPDATE_RANK["save"][0] % (obj_actor.first_name,
                                                             obj_actor.last_name,
                                                             new_rank)
                        self.view.prompt_questions(msg, "save")

        Menu(DICT_ACTORS_MENU)


class Quit():

    def __init__(self):
        self.view = Command()
        self.view.show_quit()