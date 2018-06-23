# coding=utf-8
import random


class ProbabilityMachine(object):
    """
    Create random horse races
    """
    def __init__(self):
        # 1 in 4 is a 25% probability
        self.chart = {
            1: 4.5,
            2: 6.01,
            3: 7.51,
            4: 10.51,
            5: 14.51,
            6: 15.02,
            7: 16.52,
            8: 18.02,
            9: 22.52,
            10: 30.03,
            11: 37.54,
            12: 45.04
        }

        self.cumulative_probability = {

        }
        so_far = 0
        for i in range(1, 13):
            decimal_probability = 1 / self.chart[i]
            so_far += decimal_probability
            self.cumulative_probability[i] = so_far

    def float_based_draw(self):
        draw = random.uniform(0, 1)
        for i in range(1, 13):
            if draw < self.cumulative_probability[i]:
                return i
        return -1

    def horse_order(self):
        places = {}

        rank = 1

        i = 0
        while True:
            i += 1
            if i > 1000:
                raise TypeError("Infinite loop")
            if len(places) == 11:
                missing = -1
                for horse in self.chart:
                    if horse not in places:
                        missing = horse
                places[missing] = 12
                break
            # horse = get_first_place(chart_copy)
            horse = self.float_based_draw()

            if horse == -1:
                continue
            # del chart_copy[horse]
            if horse in places:
                continue
            places[horse] = rank
            if len(places) == 12:
                break

            rank += 1
            if rank > 12:
                print(places)
                raise TypeError("uh oh")

        return places

    def sum_em(self):

        ratios = []
        for horse, probability in self.chart.items():
            ratios.append(1 / probability)

        return ratios


if __name__ == "__main__":
    machine = ProbabilityMachine()
    machine.horse_order()
    machine.sum_em()
