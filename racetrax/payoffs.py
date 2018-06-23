# coding=utf-8
"""
Payoff data files
"""

# read file
import csv

TOP = 50 + 10
BOTTOM = 50 - 10


class PayoutTables(object):
    def __init__(self):
        self.charts = {}

        # todo win, place, show

        self.exacta()
        self.trifecta()
        self.quinella()
        self.superfecta()

    # TODO: Place, Show

    def find_bets_by_prize(self, low, high):
        possible_conforming = []
        for key, value in self.charts.items():
            for row in value:
                prize = row[4]
                odds = row [5]
                if low < prize < high:
                    possible_conforming.append(row)

        return possible_conforming

    def find_bets_by_odds(self, low, high):
        possible_conforming = []
        for key, value in self.charts.items():
            for row in value:
                prize = row[4]
                odds = row [5]
                if low < odds < high:
                    possible_conforming.append(row)

        return possible_conforming

    def quinella(self):
        i = 0
        with open("../data_md/tabula-QuinellaPayouts.csv") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            data = []
            for row in reader:
                i += 1
                if i == 1:
                    # header
                    continue

                odds = float(row[3].replace(",", ""))
                prize = float(row[2].replace(",", "").strip("$ "))
                # TODO: Named tuple
                data.append([row[0], row[1], None, None, prize, odds])
        self.charts["quinella"] = data

    def exacta(self):
        """
        Import Exacta payoffs
        :return:
        """
        i = 0
        with open("../data_md/tabula-Exacta-Payout-Chart.csv") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            data = []
            for row in reader:
                i += 1
                if i == 1:
                    # header
                    continue

                odds = float(row[3].replace(",", ""))
                prize = float(row[2].replace(",", "").strip("$ "))
                # TODO: Named tuple
                data.append([row[0], row[1], None, None, prize, odds])
        self.charts["exacta"] = data

    def superfecta(self):
        i = 0

        with open("../data_md/tabula-Superfecta_Payout_Chart.csv") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            data= []
            for row in reader:
                i += 1
                if i == 1:
                    # header
                    continue
                odds = float(row[5].replace(",", ""))
                prize = float(row[4].replace(",", "").strip("$ "))
                # TODO: Named tuple
                data.append([row[0], row[1], row[2], row[3], prize, odds])
            self.charts["superfecta"] = data

    def trifecta(self):
        i = 0
        with open("../data_md/tabula-TrifectaPayouts.csv") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            data = []
            for row in reader:
                i += 1
                if i == 1:
                    # header
                    continue

                odds = float(row[4].replace(",", ""))
                prize = float(row[3].replace(",", "").strip("$ "))
                data.append([row[0], row[1], row[2], None , prize, odds])
        self.charts["trifecta"] = data


if __name__ == "__main__":
    def go():
        payoutTables = PayoutTables()
        possibles= payoutTables.find_bets_by_prize(490, 510)
        print(possibles)
    go()