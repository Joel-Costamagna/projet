#! /usr/bin/env python3
# coding=utf-8

""""
    :author joelcostamagna
    created on  2018-03-09 14:56
    :version 0.1
"""


class Bus:
    """Composant BUS de donnee, servant a propager les evenements entre les différents composants.
    Les valeurs sont mise à jour par l'appelant puis la fonction event() est appelée pour propager l'event.
        - adress
        - mode(1, 2, 8 ou 9)
        - data(si ecriture )
    La valeur resultante est disponible au retour de l'execution de la fonction
        - data si lecture
    la fonction clock() sert a propager l ’ horloge vers les composants.
    """
    _components = []
    adress = 0
    mode = 0
    data = 0

    def __init__(self):
        return

    def register(self, component):
        self._components.append(component)
        return

    def clock(self):
        if not self._components:
            return
        for component in (x for x in self._components if x.clock):
            component.clock()
        return

    def event(self):
        if not self._components:
            return
        for component in (x for x in self._components if x.event):
            component.event()
        self.mode = 0
        return
