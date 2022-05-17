from helpers.function import get_list_attribut


class Match:

    def __init__(self, tournament_id="", round_id="", match_index="", couple_id=""):
        self.tournament_id = tournament_id
        self.round_id = round_id
        self.match_index = match_index
        self.couple_id = couple_id
        self.score = ""
        self._l_attribut = get_list_attribut(self)

    def assign_score(self, score):
        if score == "1":
            self.score = ([self.score[0][0], 1], [self.score[1][0], 0])
        elif score == "2":
            self.score = ([self.score[0][0], 0], [self.score[1][0], 1])
        else:
            self.score = ([self.score[0][0], 0.5], [self.score[1][0], 0.5])

    def init_score(self):
        self.score = ([self.couple_id[0], 0], [self.couple_id[1], 0])

    def serialize(self):
        match = []
        for attribut in self._l_attribut:
            mathc_info = getattr(self, attribut)
            match.append(mathc_info)
        return match

    def deserialize(self, match_item):
        for match_info, attribut in zip(match_item, self._l_attribut):
            setattr(self, attribut, match_info)

    def __repr__(self):
        rep_match = f"\n{self.round_id} :  Match n° {self.match_index} " \
                    f": {self.score[0][0]} contre {self.score[1][0]} :" \
                    f" {self.score[0][1]} - {self.score[1][1]}"
        return rep_match
