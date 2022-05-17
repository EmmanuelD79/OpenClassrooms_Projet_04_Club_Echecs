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

    def attribut_getter(self):
        return self._l_attribut

    def update_rank(self, int_new_ranking):
        self.rank = int_new_ranking

    def serialize(self):
        '''Serialize an actor object to an actor information dictionary
        with an attributs list in order of init position'''
        dict_actor_info = {}
        for attribut in self._l_attribut:
            dict_actor_info[attribut] = getattr(self, attribut)
        return dict_actor_info

    def deserialize(self, dict_actor_info):
        '''Deserialize an actor information dictionary to actor object
        with an attributs list in order of init position'''
        l_actor_info = []
        for key in dict_actor_info:
            l_actor_info.append(dict_actor_info[key])
        for attribut, data in zip(self._l_attribut, l_actor_info):
            setattr(self, attribut, data)

    def update_db(self):
        update_actor = Query()
        dict_actor_info = self.serialize()
        ACTORS.update(dict_actor_info, update_actor.id == self.id)

    def insert_db(self):
        dict_actor_info = self.serialize()
        ACTORS.insert(dict_actor_info)

    def save_db(self):
        search_actor = Query()
        actor_item = ACTORS.search(search_actor.id == self.id)
        if actor_item:
            self.update_db()
            state = "update"
        else:
            self.insert_db()
            state = "insert"
        return state

    def load_all(self):
        dict_all_actors = {}
        for dict_actor_info in ACTORS:
            actor = Actor()
            actor.deserialize(dict_actor_info)
            dict_all_actors[actor.id] = actor
        return dict_all_actors

    def __repr__(self):
        rep_actor = f"{self.first_name}, {self.last_name}, {self.date_of_birth}, {self.sex}, {self.rank}"
        return rep_actor
