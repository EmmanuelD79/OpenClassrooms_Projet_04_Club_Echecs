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

    def create_me(self, l_players_id, l_players_points):
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

    def serialize_me(self):
        dict_tournament = {}
        for attribut in self._l_attribut:
            value = getattr(self, attribut)
            if attribut == "l_rounds":
                rounds = value
                l_rounds = []
                for round in rounds:
                    l_rounds.append(round.serialize_me())
                value = l_rounds
            dict_tournament[attribut] = value
        return dict_tournament

    def deserialize_me(self, dict_tournament):
        for attribut in self._l_attribut:
            if attribut == "l_rounds":
                l_rounds = []
                rounds = dict_tournament[attribut]
                for round_item in rounds:
                    round = Round()
                    round.deserialize_me(round_item)
                    l_rounds.append(round)
                setattr(self, attribut, l_rounds)
            else:
                setattr(self, attribut, dict_tournament[attribut])

    def update_me(self):
        update = Query()
        dict_tournament = self.serialize_me()
        TOURNAMENTS.update(dict_tournament, update.id == self.id)

    def insert_me(self):
        dict_tournament = self.serialize_me()
        TOURNAMENTS.insert(dict_tournament)

    def save_me(self):
        search_me = Query()
        tournament_item = TOURNAMENTS.search(search_me.id == self.id)
        if tournament_item:
            self.update_me()
            state = "update"
        else:
            self.insert_me()
            state = "insert"
        return state

    def load_all(self):
        dict_all_tournaments = {}
        for tournament_item in TOURNAMENTS:
            tournament = Tournament()
            tournament.deserialize_me(tournament_item)
            dict_all_tournaments[tournament.id] = tournament
        return dict_all_tournaments

    def set_points(self):
        if self.l_players_points and self.l_rounds:
            self._last_round = self.l_rounds[-1]
            for match in self._last_round.matches:
                if isinstance(match.match, tuple) and (len(match.match) == 2):
                    for player, score in match.match:
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
