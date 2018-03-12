#! /usr/bin/env python3
# coding=utf-8

""""
    :author joelcostamagna
    created on  2018-03-09 14:55
    :version 0.1
"""

from bus import Bus
from Cpu import Cpu
from rom import Rom

if __name__ == '__main__':
    # Creation du bus a la base de l ’ ordinateur pour les communications
    bus = Bus()
    # Creation du cpu en le reliant au bus
    cpu = Cpu(bus)
    # Creation de la rom en la reliant au bus
    rom = Rom(bus)  # Creation du GUI  # Connexion du GUI aux composants  #  Boucle sans fin du programme
