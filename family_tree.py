"""
Family tree
"""

import random
import math
from person_factory import PersonFactory


class FamilyTree:
    # driver class for generating/managing the family tree

    def __init__(self):
        self.factory = PersonFactory()
        self.people = []
        self.first_person = None
        self.second_person = None
        self.founding_last_names = set()

    #read all data
    def read_files(self):
        print("Reading files...")
        self.factory.read_files()

   #generate full tree

    def generate_tree(self):
        print("Generating family tree...")

        # create first two people born in 1950
        self.first_person = self.factory.get_person(1950)
        self.second_person = self.factory.get_person(1950)

        # store founding last names
        self.founding_last_names.add(self.first_person.get_last_name())
        self.founding_last_names.add(self.second_person.get_last_name())

        # make them partners
        self.first_person.set_partner(self.second_person)
        self.second_person.set_partner(self.first_person)

        self.people.extend([self.first_person, self.second_person])

        index = 0

        # expand family using growing list
        while index < len(self.people):

            person = self.people[index]
            birth_year = person.get_year_born()

            # stop if children would be born beyond 2120
            if birth_year + 25 >= 2120:
                index += 1
                continue

            decade = f"{(birth_year // 10) * 10}s"

            # stop if decade not supported in dataset
            if decade not in self.factory.birth_marriage_rates:
                index += 1
                continue

            birth_rate, marriage_rate = self.factory.birth_marriage_rates[decade]

            #try to generate partner

            if not person.has_partner():
                if random.random() <= marriage_rate:

                    partner_year = birth_year + random.randint(-10, 10)

                    # clamp to assignment range
                    if partner_year < 1950:
                        partner_year = 1950
                    if partner_year > 2120:
                        partner_year = 2120

                    partner = self.factory.get_person(partner_year)

                    person.set_partner(partner)
                    partner.set_partner(person)

                    self.people.append(partner)

            #generate children

            if person.get_num_children() == 0:

                min_children = math.ceil(birth_rate - 1.5)
                max_children = math.ceil(birth_rate + 1.5)

                num_children = random.randint(min_children, max_children)

                # CS 562 rule: one fewer child if no partner
                if not person.has_partner():
                    num_children -= 1

                if num_children > 0:

                    start_year = birth_year + 25
                    end_year = min(birth_year + 45, 2119)

                    if num_children == 1:
                        child_years = [(start_year + end_year) // 2]
                    else:
                        gap = (end_year - start_year) / (num_children - 1)
                        child_years = [
                            int(start_year + i * gap)
                            for i in range(num_children)
                        ]

                    for year in child_years:

                        # enforce founding last-name rule
                        if person.get_last_name() in self.founding_last_names:
                            child_last_name = person.get_last_name()

                        elif person.has_partner() and \
                             person.get_partner().get_last_name() in self.founding_last_names:
                            child_last_name = person.get_partner().get_last_name()

                        else:
                            # fallback
                            child_last_name = person.get_last_name()

                        child = self.factory.get_person(
                            year,
                            inherited_last_name=child_last_name
                        )

                        person.add_child(child)

                        if person.has_partner():
                            person.get_partner().add_child(child)

                        self.people.append(child)

            index += 1

    #methods

    def get_total_people(self):
        return len(self.people)

    def get_people_by_decade(self):
        counts = {}
        for person in self.people:
            decade = (person.get_year_born() // 10) * 10
            counts[decade] = counts.get(decade, 0) + 1
        return counts

    def get_duplicate_names(self):
        names = {}
        for person in self.people:
            full_name = person.get_first_name() + " " + person.get_last_name()
            names[full_name] = names.get(full_name, 0) + 1

        return sorted(
            [name for name, count in names.items() if count > 1]
        )


#main
#Code style follows PEP 8 conventions for indentation, naming, spacing, and documentation.
def main():

    #create family tree
    tree = FamilyTree()

    #read data files
    tree.read_files()

    #generate complete family tree
    tree.generate_tree()

    #interactive interface
    while True:
        print("Are you interested in:")
        print("(T)otal number of people in the tree")
        print("Total number of people in the tree by (D)ecade")
        print("(N)ames duplicated")
        print("(Q)uit")

        choice = input("> ").strip().upper()

        if choice == "T":
            print(f"The tree contains {tree.get_total_people()} people total")

        elif choice == "D":
            decades = tree.get_people_by_decade()
            for decade in sorted(decades):
                print(f"{decade}: {decades[decade]}")

        elif choice == "N":
            dups = tree.get_duplicate_names()
            print(f"There are {len(dups)} duplicate names in the tree:")
            for name in dups:
                print("*", name)

        elif choice == "Q":
            break


if __name__ == "__main__":
    main()