from models.db import TOURNAMENTS
from models.rounds import Round
from tinydb import Query
from constants.base import DEFAULT_NB_ROUND
from helpers.function import get_date_hour, get_list_attribut


class Tournament:

    def __init__(self):

        self.id = ""
        self.name = ""
        self.site = ""
        self.start = None
        self.stop = None
        self.l_players_id = []
        self.l_rounds = []
        self.nb_rounds = DEFAULT_NB_ROUND
        self.control_time = ""
        self.description = ""
        self.l_done_matches = []
        self.l_players_points = []
        self._l_attribut = get_list_attribut(self)

    def attribut_getter(self):
        return self._l_attribut

    def start_to_play(self):
        self.start = get_date_hour()

    def stop_to_play(self):
        self.stop = get_date_hour()

    def add_players(self, l_players_id, l_players_points):
        self.l_players_id = l_players_id
        self.l_players_points = l_players_points

    def add_done_match(self, done_match):
        self.l_done_matches.append(done_match)

    def add_round(self, obj_round):
        if isinstance(obj_round, object):
            self.l_rounds.append(obj_round)
            return True

    def sort_players_by_points_and_rank(self):
        l_sorted_players = []
        for id_player, score in sorted(self.l_players_points.items(),
                                       key=lambda sorting: (-sorting[1][1], sorting[1][0])):
            l_sorted_players.append(id_player)
        return l_sorted_players

    def serialize(self):
        dict_tournament_info = {}
        for attribut in self._l_attribut:
            value = getattr(self, attribut)
            if attribut == "l_rounds":
                rounds = value
                l_rounds = []
                for round in rounds:
                    l_rounds.append(round.serialize())
                value = l_rounds
            dict_tournament_info[attribut] = value
        return dict_tournament_info

    def deserialize(self, dict_tournament_info):
        for attribut in self._l_attribut:
            if attribut == "l_rounds":
                l_rounds = []
                rounds = dict_tournament_info[attribut]
                for round_item in rounds:
                    round = Round()
                    round.deserialize(round_item)
                    l_rounds.append(round)
                setattr(self, attribut, l_rounds)
            else:
                setattr(self, attribut, dict_tournament_info[attribut])

    def update_db(self):
        update_tournament = Query()
        dict_tournament_info = self.serialize()
        TOURNAMENTS.update(dict_tournament_info, update_tournament.id == self.id)

    def insert_db(self):
        dict_tournament_info = self.serialize()
        TOURNAMENTS.insert(dict_tournament_info)

    def save_db(self):
        search_tournament = Query()
        tournament_item = TOURNAMENTS.search(search_tournament.id == self.id)
        if tournament_item:
            self.update_db()
            state = "update"
        else:
            self.insert_db()
            state = "insert"
        return state

    def load_all(self):
        dict_all_tournaments = {}
        for tournament_item in TOURNAMENTS:
            tournament = Tournament()
            tournament.deserialize(tournament_item)
            dict_all_tournaments[tournament.id] = tournament
        return dict_all_tournaments

    def set_points(self):
        if self.l_players_points and self.l_rounds:
            self._last_round = self.l_rounds[-1]
            for match in self._last_round.matches:
                if isinstance(match.score, tuple) and (len(match.score) == 2):
                    for player, score in match.score:
                        self.l_players_points[player][1] += score
            return True

    def __repr__(self):
        if self.stop is None:
            txt_stop = "Le tournoi n'est pas terminé"
        else:
            txt_stop = f"le tournoi a été finalisé {self.stop}"
        txt_score = str()
        for players_id in self.l_players_id:
            player_score = self.l_players_points[players_id][1]
            txt_score += f"le joueur n°{players_id} a un score de {player_score}\n"
        rep_tournament = f"\nDébuté {self.start} \n" \
                         f"Le tournoi {self.name} à {self.site} : id = {self.id} " \
                         f"\nle score des joueurs :\n{txt_score}" \
                         f"\n{self.l_rounds}\n {txt_stop}\n"
        return rep_tournament
