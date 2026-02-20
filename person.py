"""
Person class - represents one individual in the family tree
"""

class Person:
    def __init__(self, year_born, year_died,
                 first_name, last_name, gender):

        self._year_born = year_born
        self._year_died = year_died
        self._first_name = first_name
        self._last_name = last_name
        self._gender = gender
        self._partner = None
        self._children = []

    # getter methods

    def get_year_born(self):
        return self._year_born

    def get_year_died(self):
        return self._year_died

    def get_first_name(self):
        return self._first_name

    def get_last_name(self):
        return self._last_name

    def get_gender(self):
        return self._gender

    def get_partner(self):
        return self._partner

    def get_children(self):
        return self._children

    def get_full_name(self):
        return self._first_name + " " + self._last_name

    def has_partner(self):
        return self._partner is not None

    def get_num_children(self):
        return len(self._children)

    # setter methods

    def set_year_died(self, year_died):
        self._year_died = year_died

    def set_partner(self, partner):
        self._partner = partner

    def add_child(self, child):
        self._children.append(child)