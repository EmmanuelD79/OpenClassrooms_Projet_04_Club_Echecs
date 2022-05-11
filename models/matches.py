from helpers.function import get_list_attribut


class Match:

    def __init__(self):
        self.tournament_id = ""
        self.round_id = ""
        self.match_index = ""
        self.couple_id = ""
        self.match = ""
        self._l_attribut = get_list_attribut(self)

    def assign_score(self, score):
        if score == "1":
            self.match = ([self.match[0][0], 1], [self.match[1][0], 0])
        elif score == "2":
            self.match = ([self.match[0][0], 0], [self.match[1][0], 1])
        else:
            self.match = ([self.match[0][0], 0.5], [self.match[1][0], 0.5])

    def create_me(self, tournament_id, round_id, match_index, couple_id):
        self.tournament_id = tournament_id
        self.round_id = round_id
        self.match_index = match_index
        self.couple_id = couple_id
        self.match = ([self.couple_id[0], 0], [self.couple_id[1], 0])

    def serialize_me(self):
        match = []
        for attribut in self._l_attribut:
            mathc_info = getattr(self, attribut)
            match.append(mathc_info)
        return match

    def deserialize_me(self, match_item):
        for match_info, attribut in zip(match_item, self._l_attribut):
            setattr(self, attribut, match_info)

    def __repr__(self):
        rep_match = f"\n{self.round_id} :  Match n° {self.match_index} " \
                    f": {self.match[0][0]} contre {self.match[1][0]} :" \
                    f" {self.match[0][1]} - {self.match[1][1]}"
        return rep_match
