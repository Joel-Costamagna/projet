#! /usr/bin/env python3
# coding=utf-8

""""
    :author joelcostamagna
    created on  2018-03-09 14:58
    :version 0.1
"""


class Rom:

    def __init__(self, bus):
        bus.register()
        return

    def event(self):
        """traitement des évenements du bus"""
        return

    def clock(self):
        return

    def run(self):
        return
