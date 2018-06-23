# coding=utf-8
"""
Basic respresentation of game and payoffs
"""
from racetrax.number_machine import ProbabilityMachine


class Player(object):
    """
    Represents a gambler playing same ticket/strategy until win or ruin.
    """
    def __init__(self, max_loss, max_plays, max_ticket, max_win):
        self.max_loss = max_loss
        self.max_plays = max_plays
        self.max_ticket = max_ticket
        self.max_win = max_win

        # when this hits zero, game over
        self.bank_account = max_loss
        self.plays = 0

    def good_game(self):
        return self.bank_account >= self.max_win

    def stop_game(self):
        if self.bank_account < 0:
            return True
        if self.plays > self.max_plays:
            return True


class Racetrax(object):
    """
    Represents rules of game
    """
    def __init__(self):
        self.outcome = []

    def draw(self):
        machine = ProbabilityMachine()
        self.outcome = machine.horse_order()

    def check_ticket(self, ticket):
        """

        :type ticket: Ticket
        :return: int
        """

        # lookup in payoff charts for each game type.
