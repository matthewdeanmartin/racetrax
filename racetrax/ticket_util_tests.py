# coding=utf-8
"""
Exercise code
"""

from racetrax.ticket_utils import Ticket


def test_creation():
    """
    Non rigorously check code
    :return:
    """
    ticket = Ticket()
    ticket.randomize()
    ticket.is_rational(0)
    ticket.is_valid()


def test_price():
    """
    Can price be called at all
    :return:
    """
    ticket = Ticket()
    ticket.randomize()
    ticket.price()
