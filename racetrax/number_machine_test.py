# coding=utf-8

from racetrax.number_machine import ProbabilityMachine


def test_if_chart_makes_sense():
    """
    Expect probabilities to add up to 1
    :return:
    """
    machine = ProbabilityMachine()
    print(machine.sum_em())
    print(sum(machine.sum_em()))


def test_if_match():
    """
    Expect theoretical to add up to
    :return:
    """
    machine = ProbabilityMachine()
    races = []
    j = 0
    iterations = 20000
    while j < iterations:
        race = machine.horse_order()
        races.append(race)
        j += 1

    win_count = {}
    for i in range(1, 13):
        win_count[i] = 0
    for race in races:
        # print(race)
        for horse, spot in race.items():
            if spot == 1:
                win_count[horse] += 1
                # continue
    print(

        "win count before normalization"
    )
    print(win_count)
    for horse, wins in win_count.items():
        win_count[horse] = "{0:.3f}".format(win_count[horse] / len(races))

    sums = machine.sum_em()
    for i in range(1, 13):
        print("horse", "emp", "expected", "dif")
        print(i, win_count[i], "{0:.3f}".format(sums[i - 1]),
              "{0:.4f}".format(abs((float(win_count[i]) - float(sums[i - 1]))) / float(sums[i - 1])))
