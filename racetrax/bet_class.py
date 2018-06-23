# coding=utf-8
"""
A single type of bet EXCLUDING combination bets.
"""

class Bet(object):
    def __init__(self):
        self.bet_type = None
        self.amount = 1
        self.boxes = (0,0,0,0)

        self.ranges = {  "bet_type": [
                # 1 horse in 1st place. Can pick more than 1!
                "Win",
                # 1 horse in 1st, 2nd, 3rd. Can pick more than 1!
                "Show",
                # combinations of horses in 1st, 2nd, 3rd...confusing
                "Win/Show",  # Can pick more than 1!

                # 1st two, and in order
                "Exacta",

                # 1st two, but not in order
                "Quinella",

                # 1st 3, and in order
                "Trifecta",

                # 1st 4, in order
                "Superfecta"
            ],
        }
