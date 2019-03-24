#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Génération de texte
# Copyright (C) 2019 Ewenak@github
#
# Génération de texte is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Génération de texte is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Génération de texte; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#

from texte import genere_phrase, finalise_phrase
import random
import speake3

phrases = []
if __name__ == '__main__':
    for x in range(0, 100):
        phrase = genere_phrase()
        phrases.append(finalise_phrase(phrase))
        print(phrases[-1])
        
    e = speake3.Speake()
    e.set('voice', 'fr')
    for i in range(0, 5):
        e.say(random.choice(phrases))
    e.talkback()