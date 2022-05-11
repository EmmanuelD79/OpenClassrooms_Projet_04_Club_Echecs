from models.db import ACTORS
from tinydb import Query
from helpers.function import get_list_attribut


class Actor:

    def __init__(self):
        self.id = ""
        self.first_name = ""
        self.last_name = ""
        self.date_of_birth = ""
        self.sex = ""
        self.rank = ""
        self._l_attribut = get_list_attribut(self)

    def update_rank(self, int_new_ranking):
        self.rank = int_new_ranking

    def serialize_me(self):
        dict_actors = {}
        for attribut in self._l_attribut:
            dict_actors[attribut] = getattr(self, attribut)
        return dict_actors

    def deserialize_me(self, dict_actors):
        actors = []
        for key in dict_actors:
            actors.append(dict_actors[key])
        for attribut, data in zip(self._l_attribut, actors):
            setattr(self, attribut, data)

    def update_me(self):
        update = Query()
        dict_actor = self.serialize_me()
        ACTORS.update(dict_actor, update.id == self.id)

    def insert_me(self):
        dict_actor = self.serialize_me()
        ACTORS.insert(dict_actor)

    def save_me(self):
        search_me = Query()
        actor_item = ACTORS.search(search_me.id == self.id)
        if actor_item:
            self.update_me()
            state = "update"
        else:
            self.insert_me()
            state = "insert"
        return state

    def load_all(self):
        dict_all_actors = {}
        for actor_item in ACTORS:
            actor = Actor()
            actor.deserialize_me(actor_item)
            dict_all_actors[actor.id] = actor
        return dict_all_actors

    def __repr__(self):
        rep_actor = f"{self.first_name}, {self.last_name}, {self.date_of_birth}, {self.sex}, {self.rank}"
        return rep_actor
