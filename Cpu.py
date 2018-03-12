#! /usr/bin/env python3
# coding=utf-8

""""
    :author joelcostamagna
    created on  2018-03-09 14:58
    :version 0.1
"""
from alu import Alu


class Cpu:

    def __init__(self, bus):
        bus.register(self)
        self._alu = Alu()
        return

    def register(self, component):
        """Enregistre les extensions (par exemple ALU)."""
        return

    def event(self):
        return

    def clock(self):
        """Machine d'état du CPU"""
        return
