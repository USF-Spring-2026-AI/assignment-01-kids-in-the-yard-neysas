"""
PersonFactory- reads CSV files and creates Person objects.
"""

import csv
import random
from person import Person


class PersonFactory:

    def __init__(self):
        self.life_expectancy = {}
        self.birth_marriage_rates = {}
        self.first_names = []
        self.last_names = []
        self.rank_probabilities = []
        self.gender_name_probability = {}

    def read_files(self):
        # Open file and close when done
        with open("life_expectancy.csv", newline="") as f:
            # CSV reading pattern:https://docs.python.org/3/library/csv.html
            reader = csv.DictReader(f)
            for row in reader:
                self.life_expectancy[int(row["Year"])] = float(
                    row["Period life expectancy at birth"]
                )

        with open("birth_and_marriage_rates.csv", newline="") as f:
            # CSV reading pattern: https://docs.python.org/3/library/csv.html
            reader = csv.DictReader(f)
            for row in reader:
                self.birth_marriage_rates[row["decade"]] = (
                    float(row["birth_rate"]),
                    float(row["marriage_rate"])
                )

        with open("first_names.csv", newline="") as f:
            # CSV reading pattern:https://docs.python.org/3/library/csv.html
            reader = csv.DictReader(f)
            for row in reader:
                self.first_names.append(row)

        with open("last_names.csv", newline="") as f:
            # CSV reading pattern:https://docs.python.org/3/library/csv.html
            reader = csv.DictReader(f)
            for row in reader:
                self.last_names.append(row)

        with open("rank_to_probability.csv", newline="") as f:
            # CSV reading pattern:https://docs.python.org/3/library/csv.html
            reader = csv.reader(f)
            self.rank_probabilities = [float(p) for p in next(reader)]

        with open("gender_name_probability.csv", newline="") as f:
            # CSV reading pattern:https://docs.python.org/3/library/csv.html
            reader = csv.DictReader(f)
            for row in reader:
                self.gender_name_probability[row["decade"]] = float(row["probability"])

    def generate_gender(self, decade):
        male_probability = self.gender_name_probability[decade]
        if random.random() <= male_probability:
            return "male"
        return "female"

    def generate_first_name(self, decade, gender):
        names = []
        weights = []

        for row in self.first_names:
            if row["decade"] == decade and row["gender"] == gender:
                names.append(row["name"])
                weights.append(float(row["frequency"]))

        return random.choices(names, weights=weights, k=1)[0]

    def generate_last_name(self, decade, inherited_last_name=None):
        if inherited_last_name is not None:
            return inherited_last_name

        names = []
        weights = []

        for row in self.last_names:
            if row["Decade"] == decade:
                rank = int(row["Rank"])
                names.append(row["LastName"])
                weights.append(self.rank_probabilities[rank - 1])

        return random.choices(names, weights=weights, k=1)[0]

    def generate_death_year(self, year_born):
        # round birth year down to nearest decade
        decade_year = (year_born // 10) * 10

        # get life expectancy for that decade
        life_expectancy = self.life_expectancy[decade_year]

        # add random variation of +/- 10 years
        variation = random.uniform(-10, 10)

        return int(year_born + life_expectancy + variation)

    def get_person(self, year_born, inherited_last_name=None):
        decade = f"{(year_born // 10) * 10}s"

        gender = self.generate_gender(decade)
        first_name = self.generate_first_name(decade, gender)
        last_name = self.generate_last_name(decade, inherited_last_name)
        year_died = self.generate_death_year(year_born)

        return Person(year_born, year_died, first_name, last_name, gender)