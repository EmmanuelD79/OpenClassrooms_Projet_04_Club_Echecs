from helpers.function import get_date_hour, get_list_attribut
from models.matches import Match


class Round:

    def __init__(self):
        self.tournament_id = ""
        self.l_players_id = []
        self.round_n = ""
        self.id = ""
        self.start = None
        self.matches = []
        self.stop = None
        self._l_attribut = get_list_attribut(self)

    def start_to_play(self):
        self.start = get_date_hour()

    def stop_to_play(self):
        self.stop = get_date_hour()

    def pair_players(self, list_sort_players):
        if self.round_n == 1:
            slicing = int(len(list_sort_players) / 2)
            list_1 = list_sort_players[:slicing]
            list_2 = list_sort_players[slicing:]
            couple = [list_1[0], list_2[0]]
        else:
            couple = [list_sort_players[0], list_sort_players[1]]
        return couple

    def create_me(self, tournament_id, list_sort_players, round_n):
        self.tournament_id = tournament_id
        self.round_n = round_n
        self.id = "Round %i" % (self.round_n)
        self.l_players_id = list_sort_players

    def create_match(self, couple_id, match_index):
        match = Match()
        match.create_me(self.tournament_id, self.id, match_index, couple_id)
        self.matches.append(match)

    def add_matches(self, l_matches):
        self.matches = l_matches

    def serialize_me(self):
        round = {}
        for attribut in self._l_attribut:
            if attribut == "matches":
                matches = getattr(self, attribut)
                l_matches = []
                for match in matches:
                    l_matches.append(match.serialize_me())
                value = l_matches
            else:
                value = getattr(self, attribut)
            round[attribut] = value
        return round

    def deserialize_me(self, round_item):
        for round_key, attribut in zip(round_item, self._l_attribut):
            if attribut == "matches":
                l_matches = []
                matches = round_item[round_key]
                for match_item in matches:
                    match = Match()
                    match.deserialize_me(match_item)
                    l_matches.append(match)
                setattr(self, attribut, l_matches)
            else:
                setattr(self, attribut, round_item[round_key])

    def __repr__(self):
        if self.stop is None:
            txt_stop = "Le tour n'est pas terminé"
        else:
            txt_stop = f"le tour a été finalisé {self.stop}"
        rep_round = f"\n{self.start}" \
                    f"\n{self.id} a généré les matches:\n {self.matches} \n  " \
                    f"{txt_stop} "
        return rep_round
