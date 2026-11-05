# -*- coding: utf-8 -*-
# zip()
# 知識點 id: f_zip  |  講義程式

positions = ['Pitcher', 'Shortstop', 'Third Baseman']
players = ['Chien-Ming Wang', 'Derek Jeter', 'A. Rod']
for pos, player in zip(positions, players):
    print('Who is the {0}? It is {1}.'.format(pos, player))
