# coding=utf-8
"""
Anything related to filling in a valid ticket.
"""

import random


class Ticket(object):
    """
    Represents bet, games, which bet type, and four boxes of 12 numbers each.
    """

    def is_box(self):
        """
        All horses for at least 1 box
        :return:
        """
        for x in range(1, 4 + 1):
            if len(self.box[x]) == 12:
                return True

    def valid_quinella(self):
        """

        :return:
        """
        if len(self.box[1]) >= 1 and \
                len(self.box[2]) >= 1:
            return True
        if len(self.box[1]) == 0 or \
                len(self.box[2]) == 0:
            print("Need to pick at least 1 horse for 1st and 2nd.")
        if len(self.box[3]) >= 0 or \
                len(self.box[4]) >= 0:
            print("Confused, 3rd or 4th box have entries")
        return False

    def __init__(self):
        self.bet_type = ""
        self.bet = 0
        self.races = 0
        self.bonus = False

        self.choice_ranges = {

            # also called boxes. Can select more than one.
            "first": list(range(0, 13)),
            "second": list(range(0, 13)),
            "third": list(range(0, 13)),
            "forth": list(range(0, 13)),
            "bet": [.1, .50, 1, 2, 3, 4, 5, 10, 20],
            "bonus": [True, False],
            "races": [1, 2, 3, 4, 5, 10, 20],
        }

    def randomize(self):

        i = 0

        while i == 0 or not self.is_valid():
            i += 1
            for key, value in self.choice_ranges.items():
                if key not in ["first", "second", "third", "forth"]:
                    setattr(self, key, self.choice_ranges[key][random.randint(0, len(value) - 1)])
            for key, value in self.choice_ranges.items():
                if key in ["first", "second", "third", "forth"]:
                    for x in range(1, 4 + 1):
                        if self.bet in [.1, .5]:
                            is_wheel_or_box = True

                        if self.bet_type in ["Win", "Show", "Win/Show"]:
                            self.box[1].append(random.randint(0, 12))

                        if self.bet_type == "Exacta":
                            first = random.randint(0, 12)
                            second = -1
                            while second == -1:
                                pick = random.randint(0, 12)
                                if pick != first:
                                    second = pick
                            self.box[1].append(first)
                            self.box[2].append(second)

            if i > 100:
                raise TypeError("100 iterations, couldn't make a good ticket")

    def price(self):
        if self.bet_type == "Win":
            base = self.bet * self.races * len(self.first)
        elif self.bet_type == "Show":
            base = self.bet * self.races * len(self.first)

        elif self.bet_type == "Win/Show":
            # PSEUDO CODE!
            combinations = len(self.first) * len(self.second)
            base = self.bet * self.races * combinations
        elif self.bet_type == "Exacta":
            combinations = len(self.first) * len(self.second)
            base = self.bet * self.races * combinations
        elif self.bet_type == "Quinella":
            combinations = len(self.first) * len(self.second)
            base = self.bet * self.races * combinations
        elif self.bet_type == "Trifecta":
            combinations = len(self.first) * len(self.second) \
                           * len(self.third)
            base = self.bet * self.races * combinations
        elif self.bet_type == "Superfecta":
            combinations = len(self.first) * len(self.second) \
                           * len(self.third) * len(self.forth)
            base = self.bet * self.races * combinations
        else:
            raise TypeError("Invalid bet type")

        # wheel & box
        # depends on combinations
        if self.bonus:
            return base * 2
        return base

    def is_valid(self):
        if self.bet_type == "Win":
            # pick 1 in box 1
            return len(self.first) >= 1 and \
                   len(self.second) == 0 and \
                   len(self.third) == 0 and \
                   len(self.forth) == 0
        if self.bet_type == "Show":
            # pick 1 in box 1
            return len(self.first) >= 1 and \
                   len(self.second) == 0 and \
                   len(self.third) == 0 and \
                   len(self.forth) == 0

        if self.bet_type == "Quinella":
            return self.valid_quinella()

        return True

    def is_rational(self, minimum):
        """
        $640,248 is the maximum prize per race on any one ticket without Bonus; $6,502,480 with Bonus.
        :return:
        """
        # can win minimum

        # max prize isn't disallowed
        return True

    def check_rules(self):
        if self.price() > 100:
            raise TypeError("Bet too large")

    def __str__(self):
        result = "-----Ticket-----"
        for key in sorted(self.choice_ranges):
            result += "{0}, {1}".format(key, getattr(self, key))
            result += "\n"
        result += "----------------"
        return result
