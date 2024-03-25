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

from __future__ import annotations    # allows `def func(self, arg: Class)` inside of Class

import dataclasses
from dataclasses import dataclass
from enum import Enum, auto
import random
import re
import typing


VOWELS = 'aeiouyéèà'


class Genre(Enum):
    FEMININE = auto()
    MASCULINE = auto()


class Number(Enum):
    SINGULAR = auto()
    PLURAL = auto()


@dataclass
class Word:
    string: str

    def match_to_following_word(self, word: Word | str) -> str:
        return f'{self.string} '


class PluralMixin:
    als_plurals_list = ['aval', 'bal', 'banal', 'bancal', 'cal', 'carnaval', 'cérémonial', 'choral', 'étal', 'fatal', 'festival',
                        'natal', 'naval', 'récital', 'régal', 'tonal', 'pal', 'val', 'virginal']
    aux_plurals_list = ['bail', 'corail', 'émail', 'gemmail', 'soupirail', 'travail', 'vantail', 'vitrail']
    eus_aus_plurals_list = ['bleu', 'émeu', 'landau', 'lieu', 'pneu', 'sarrau']
    oux_plurals_list = ['bijou', 'caillou', 'chou', 'genou', 'hibou', 'joujou', 'pou']

    @property
    def als_plural(self):
        return self.string in self.als_plurals_list

    @property
    def aux_plural(self):
        return self.string in self.aux_plurals_list

    @property
    def eus_aus_plural(self):
        return self.string in self.eus_aus_plurals_list

    @property
    def oux_plural(self):
        return self.string in self.oux_plurals_list

    def plural(self) -> Word:
        '''This function takes a singular adjective or noun as input and returns it in plural'''
        if self.string[-1] in 'szx':
            plural_string = self.string
        elif (self.string[-2:] in ['au', 'eu'] or self.oux_plural) and not self.eus_aus_plural:
            plural_string = self.string + 'x'
        elif self.string[-2:] == 'al' and not self.als_plural:
            plural_string = self.string[:-2] + 'aux'
        elif self.aux_plural:
            plural_string = self.string[:-3] + 'aux'
        else:
            plural_string = self.string + 's'
        return dataclasses.replace(self, string=plural_string, number=Number.PLURAL)


@dataclass
class Noun(Word, PluralMixin):
    genre: Genre
    number: Number


@dataclass
class Specifier(Word):
    genre: Genre
    number: Number

    _modified_before_vowels_list = {
        'le': "l'", 'la': "l'", 'ma': 'mon ', 'sa': 'son ', 'ta': 'ton ', 'ce': 'cet ',
    }

    def match_to_following_word(self, word: Word | str) -> str:
        if isinstance(word, Word):
            word = word.string
        if word[0] in VOWELS and self.string in self._modified_before_vowels_list:
            return self._modified_before_vowels_list[self.string]
        return super().match_to_following_word(word)


@dataclass
class Adjective(Word, PluralMixin):
    genre: Genre
    number: Number

    _modified_before_vowels_list: typing.ClassVar = {'beau': 'bel ', 'nouveau': 'nouvel ', 'vieux': 'vieil '}
    _before_noun_list: typing.ClassVar = ['beau', 'grand', 'belle', 'grande']

    @property
    def before_noun(self):
        return self.string in self._before_noun_list

    def match_to_following_word(self, word: Word | str) -> str:
        if isinstance(word, Word):
            word = word.string
        if word[0] in VOWELS and word in self._modified_before_vowels_list:
            return self._modified_before_vowels_list[word]
        return super().match_to_following_word(word)


@dataclass
class WordGroup:
    words: list[Word]

    def __str__(self):
        word_string = []
        prev_word = self.words[0]
        for word in self.words:
            word_string.append(word.match_to_following_word(prev_word))
            prev_word = word
        return ''.join(word_string)


@dataclass
class NounGroup(WordGroup):
    number: Number = None
    genre: Genre = None

    def __post_init__(self):
        self.specifier = None
        self.noun = None
        self.adjectives = []
        for w in self.words:
            if isinstance(w, Specifier):
                self.specifier = w
            elif isinstance(w, Noun):
                self.noun = w
            elif isinstance(w, Adjective):
                self.adjectives.append(w)

        if self.number is None:
            self.number = self.noun.number
        if self.genre is None:
            self.genre = self.noun.genre


# Données

# True : verbe transitif
# False : verbe intransitif
verbes = {
    'manger': {'groupe': 1, 'radical': 'mang', 'transitif': True, 'pronominal': False},
    'courir': {'groupe': 3, 'radical': 'cour', 'transitif': False, 'pronominal': False},
    'dormir': {'groupe': 3, 'radical': 'dor', 'transitif': False, 'pronominal': False},
    'marcher': {'groupe': 1, 'radical': 'march', 'transitif': False, 'pronominal': False},
    'faire': {'groupe': 3, 'radical': 'fai', 'transitif': True, 'pronominal': False},
    'fabriquer': {'groupe': 1, 'radical': 'fabriqu', 'transitif': True, 'pronominal': False},
    'rigoler': {'groupe': 1, 'radical': 'rigol', 'transitif': False, 'pronominal': False},
    'parler': {'groupe': 1, 'radical': 'parl', 'transitif': False, 'pronominal': True},
    'boire': {'groupe': 3, 'radical': 'boi', 'transitif': True, 'pronominal': False},
    'casser': {'groupe': 1, 'radical': 'cass', 'transitif': True, 'pronominal': False},
    'applaudir': {'groupe': 2, 'radical': 'applaud', 'transitif': True, 'pronominal': False},
    'être': {'groupe': 3, 'radical': '', 'transitif': True, 'pronominal': False},
    'sculpter': {'groupe': 1, 'radical': 'sculpt', 'transitif': True, 'pronominal': False},
    'prendre': {'groupe': 3, 'radical': 'prend', 'transitif': True, 'pronominal': False},
    'souvenir': {'groupe': 3, 'radical': 'souv', 'transitif': False, 'pronominal': True},
    'avoir': {'groupe': 3, 'radical': '', 'transitif': True, 'pronominal': False},
    'enclencher': {'groupe': 1, 'radical': 'enclench', 'transitif': True, 'pronominal': False},
}
verbes_transitifs = [k for k, v in verbes.items() if v['transitif']]
conjugaisons = {
    'indicatif': {
        'present': {
            1: ['e', 'es', 'e', 'ons', 'ez', 'ent'],
            2: ['is', 'is', 'it', 'issons', 'issez', 'issent']
        },
        'imparfait': {
            1: ['ais', 'ais', 'ait', 'ions', 'iez', 'aient'],
            2: ['issais', 'issais', 'issait', 'issions', 'issiez', 'issaient']
        }
    },
    'participe': {
        'passe': {
            1: 'é',
            2: 'i',
        },
    }
}

temps_implementes = {'present': "Présent de l'indicatif",
                     'imparfait': "Imparfait de l'indicatif",
                     'passe_compose': 'Passé composé'}

conjug_3e = {'boire': {'indicatif': {'present': ['bois', 'bois', 'boit', 'buvons', 'buvez', 'boivent'],
                                     'imparfait': ['buvais', 'buvais', 'buvait', 'buvions', 'buviez', 'buvaient']},
                       'participe': {'passe': 'bu'}},
             'courir': {'indicatif': {'present': ['cours', 'cours', 'court', 'courons', 'courez', 'courent'],
                                      'imparfait': ['courais', 'courais', 'courait', 'courions', 'couriez', 'couraient']},
                        'participe': {'passe': 'couru'}},
             'dormir': {'indicatif': {'present': ['dors', 'dors', 'dort', 'dormons', 'dormez', 'dorment'],
                                      'imparfait': ['dormais', 'dormais', 'dormait', 'dormions', 'dormiez', 'dormaient']},
                        'participe': {'passe': 'dormi'}},
             'faire': {'indicatif': {'present': ['fais', 'fais', 'fait', 'faisons', 'faites', 'font'],
                                     'imparfait': ['faisais', 'faisais', 'faisait', 'faisions', 'faisiez', 'faisaient']},
                       'participe': {'passe': 'fait'}},
             'être': {'indicatif': {'present': ['suis', 'es', 'est', 'sommes', 'êtes', 'sont'],
                                    'imparfait': ['étais', 'étais', 'était', 'étions', 'étiez', 'étaient']},
                      'participe': {'passe': 'été'}},
             'prendre': {'indicatif': {'present': ['prends', 'prends', 'prend', 'prenons', 'prenez', 'prennent'],
                                       'imparfait': ['prenais', 'prenais', 'prenait', 'prenions', 'preniez', 'prenaient']},
                         'participe': {'passe': 'pris'}},
             'souvenir': {'indicatif': {'present': ['souviens', 'souviens', 'souviens', 'souvenons', 'souvenez', 'souviennent'],
                                        'imparfait': ['souvenais', 'souvenais', 'souvenait', 'souvenions', 'souveniez', 'souvenaient']},
                          'participe': {'passe': 'souvenu'}},
             'avoir': {'indicatif': {'present': ['ai', 'as', 'a', 'avons', 'avez', 'ont'],
                                     'imparfait': ['avais', 'avais', 'avait', 'avions', 'aviez', 'avaient']},
                       'participe': {'passe': 'eu'}}}

noms = {
    Genre.FEMININE: ['nourriture', 'couverture', 'arrivée', 'tente', 'voiture', 'nature', 'discussion', 'éternité',
                     'bonté'],
    Genre.MASCULINE: ['papier', 'ordinateur', 'mot', 'casse-croûte', 'véhicule', 'métier', 'verre', 'bois', 'boa', 'schtroumpf',
                      'remède', 'zéro', 'masseur', 'lit', 'pneu', 'jeu'],
}

adjectifs = {
    Genre.FEMININE: ['noire', 'bleue', 'belle', 'rigolote', 'bizarre', 'bretonne', 'lumineuse', 'grande', 'transparente',
                     'énorme', 'schtroumpf', 'sage', 'embêtante', 'faible', 'fainéante', 'grossière'],
    Genre.MASCULINE: ['noir', 'bleu', 'beau', 'rigolo', 'bizarre', 'breton', 'lumineux', 'grand', 'transparent', 'énorme',
                      'schtroumpf', 'sage', 'embêtant', 'faible', 'fainéant', 'grossier'],
}
pronoms_personnels = {'je': 0, 'tu': 1, 'il': 2, 'elle': 2, 'nous': 3, 'vous': 4, 'ils': 5, 'elles': 5}
pronoms_personnels_reflechis = ['me', 'te', 'se', 'nous', 'vous', 'se']
determinants = {Genre.MASCULINE: ['le', 'un', 'mon', 'ce', 'notre', 'votre', 'son', 'ton', 'leur', 'quelque'],
                Genre.FEMININE: ['la', 'une', 'ma', 'cette', 'notre', 'votre', 'sa', 'ta', 'leur', 'quelque'],
                Number.PLURAL: ['les', 'des', 'mes', 'ces', 'nos', 'vos', 'ses', 'tes', 'leurs', 'quelques']}
adverbes = ['rapidement', 'bien', 'bruyamment', 'calmement', 'sans effort', 'schtroumpfement', 'jeunement',
            'perpétuellement', 'fatalement', 'épisodiquement', 'farouchement', 'intégralement',
            'individuellement', 'anticonstitutionnellement']
prepositions_lieu = ['à', 'sur', 'dans']
structures_phrase = [['sgn', 'v', 'adv'], ['sgn', 'v'], ['sgn', 'vt', 'cod'], ['sgn', 'vt', 'cod', 'adv'],
                     ['adv', ',', 'sgn', 'v'], ['pp', 'v'], ['pp', 'v', 'adv'], ['pp', 'vt', 'cod', 'adv'],
                     ['adv', ',', 'pp', 'vt', 'cod'], ['sgn', 'vt', 'cod', 'ccl'], ['pp', 'vt', 'cod', 'adv', 'ccl'],
                     ['adv', ',', 'sgn', 'vt', 'cod', 'ccl']]


class EmptyRootError(NameError):
    pass


def noun_group(specifier=None, noun=None, adj=None, genre=None, number=None):
    '''Renvoie un groupe nominal (gn) dont on peut spécifier certaines choses'''
    gn = []
    # Genre detection
    if genre is None:
        genre = next((w.genre for w in [specifier, noun, adj] if w is not None), None)
        if genre is None:
            genre = random.choice(list(Genre))

    if number is None:
        number = next((w.number for w in [specifier, noun, adj] if w is not None), None)
        if number is None:
            number = random.choice(list(Number))

    if specifier is None:
        specifier = Specifier(
            random.choice(determinants[genre]) if number == Number.SINGULAR else random.choice(determinants[number]),
            genre=genre, number=number)
    if adj is None:
        adj = Adjective(random.choice(adjectifs[genre]), genre=genre, number=number)
    if noun is None:
        noun = Noun(random.choice(noms[genre]), genre=genre, number=number)

    # Plural
    if number == Number.PLURAL:
        adj = adj.plural()
        noun = noun.plural()

    if adj.before_noun:
        words = [specifier, adj, noun]
    else:
        words = [specifier, noun, adj]

    return NounGroup(words=words)


def conjugaison(verbe, personne=None, temps='present', ajouter_pronoms=True):
    '''Conjugue le verbe passé en paramètre
    au temps et à la personne voulus'''
    if personne is None and temps != 'participe_passe':
        return verbe
    verbe_conjugue = []
    if isinstance(verbe, dict):
        cara_verbe = verbe
    else:
        if verbe in verbes:
            cara_verbe = verbes[verbe]
        else:
            m = re.search(r'(.+)([ei]r)$', verbe)
            if m is not None:
                radical, terminaison = m.groups()
                if terminaison == 'er':
                    groupe = 1
                else:
                    groupe = 2
            else:
                return verbe
            cara_verbe = {'groupe': groupe, 'radical': radical, 'transitif': False, 'pronominal': False}
    radical = cara_verbe['radical']
    groupe = cara_verbe['groupe']
    if groupe == 3:
        if temps == 'participe_passe':
            if isinstance(verbe, dict):
                verbe_conjugue = verbe['conjugaisons']['participe']['temps']
            else:
                verbe_conjugue = conjug_3e[verbe]['participe']['passe']
        elif temps == 'passe_compose':
            if isinstance(verbe, dict):
                verbe_conjugue = conjugaison('être' if verbe['pronominal'] else 'avoir', personne) + ' ' + conjugaison(verbe, 0, temps='participe_passe', ajouter_pronoms=False)
            else:
                verbe_conjugue = conjugaison('être' if verbes[verbe]['pronominal'] else 'avoir', personne) + ' ' + conjugaison(verbe, 0, temps='participe_passe', ajouter_pronoms=False)
        else:
            if isinstance(verbe, dict):
                verbe_conjugue = verbe['conjugaisons']['indicatif'][temps][personne]
            else:
                verbe_conjugue = conjug_3e[verbe]['indicatif'][temps][personne]
    else:
        if temps == 'participe_passe':
            return radical + conjugaisons['participe']['passe'][groupe]
        elif temps == 'passe_compose':
            verbe_conjugue = conjugaison('être' if verbes[verbe]['pronominal'] else 'avoir', personne) + ' ' + conjugaison(verbe, temps='participe_passe', ajouter_pronoms=False)
        else:
            terminaison = conjugaisons['indicatif'][temps][groupe][personne]
            if radical == '':
                raise EmptyRootError(verbe)
            if groupe == 1:
                verbe_conjugue = radical + ('e' if (terminaison[0] in ['a', 'o', 'u'] and radical[-1] == 'g') else '') + terminaison
            elif groupe == 2:
                verbe_conjugue = radical + terminaison
    if ajouter_pronoms:
        if cara_verbe['pronominal']:
            if not verbe_conjugue[0] in VOWELS or not pronoms_personnels_reflechis[personne][-1] in VOWELS:
                verbe_conjugue = pronoms_personnels_reflechis[personne] + ' ' + verbe_conjugue
            else:
                verbe_conjugue = pronoms_personnels_reflechis[personne][:-1] + "'" + verbe_conjugue
    return verbe_conjugue


def complement_lieu(prep=None, gn=None):
    'Génère complément circonstanciel de temps'
    if prep is None:
        prep = random.choice(prepositions_lieu)
    if gn is None:
        gn = noun_group()
    if prep == 'à':
        if gn['contenu'][0] == 'le':
            prep = 'au'
            gn['det'] = ''
            gn['contenu'][0] = ''
        elif gn['contenu'][0] == 'les':
            prep = 'aux'
            gn['det'] = ''
            gn['contenu'][0] = ''
    complement = [prep] + gn['contenu']
    return {'contenu': complement, 'prep': prep, 'cod': gn}


def genere_phrase(structure=None, temps=None, question=None, negatif=None, mot_negation=None, sujet=None, verbe=None, cod=None, adv=None, ccl=None):
    'Génère une phrase'
    phrase = []
    pas_de_structure = all(var is None for var in (structure, sujet, verbe, cod,
                                                   adv, ccl))
    if pas_de_structure:
        structure_phrase = random.choice(structures_phrase)
    else:
        if structure is not None:
            structure_phrase = structure
        else:
            contenu_min = set()
            if sujet is not None:
                if isinstance(sujet, str):
                    contenu_min.add('pp')
                else:
                    contenu_min.add('sgn')
            if verbe is not None:
                if verbe in verbes_transitifs:
                    contenu_min.add('vt')
                else:
                    contenu_min.add('v')
            if cod is not None:
                contenu_min.add('cod')
            if adv is not None:
                contenu_min.add('adv')
            if ccl is not None:
                contenu_min.add('ccl')
            structures_possibles = [s for s in structures_phrase if contenu_min.issubset(set(s))]
            structure_phrase = random.choice(structures_possibles)

    transitif = 'vt' in structure_phrase

    if temps is None:
        temps = random.choice(list(temps_implementes.keys()))
    if question is None:
        question = random.choice([False, False, True])
    if question:
        if 'pp' in structure_phrase:
            if transitif:
                nouvelle_structure = ['vt', '-', 'pp']
            else:
                nouvelle_structure = ['v', '-', 'pp']
        else:
            if transitif:
                nouvelle_structure = ['Est-ce que', 'sgn', 'vt']
            else:
                nouvelle_structure = ['Est-ce que', 'sgn', 'v']
        for c in ['cod', 'adv', 'ccl']:
            if c in structure_phrase:
                nouvelle_structure.append(c)
        nouvelle_structure.append('?')
        structure_phrase = nouvelle_structure
    if negatif is None and mot_negation is None:
        negatif = random.choice([False, True])
    elif mot_negation is not None and negatif:
        negatif = True
    if negatif and mot_negation is None:
        mot_negation = random.choice(['pas', 'plus', 'jamais', 'presque plus', 'presque jamais'])

    if verbe is None:
        verbe_infinitif = (random.choice([v for v in verbes.keys() if v != 'être' and v != 'avoir']) if 'v' in structure_phrase
                           else random.choice(verbes_transitifs))
    else:
        verbe_infinitif = verbe
        if not isinstance(verbe, dict) and verbe not in verbes:
            print(f"""Ce programme ne connais pas le verbe {verbe}. \
Il est possible de passer un dictionnaire en paramètre avec les champs \
infinitif (str), groupe (int), radical (str), transitif (bool) et pronominal (bool) et aussi, \
si le verbe est du troisième groupe, conjugaisons (list).""")
            return None

    if 'pp' in structure_phrase:
        nature_sujet = 'pp'
    else:
        nature_sujet = 'gn'

    # Définition de la personne
    if sujet is None:
        if nature_sujet == 'pp':
            sujet = random.choice(list(pronoms_personnels.keys()))
            personne = pronoms_personnels[sujet]
        else:
            sujet = noun_group()
            if sujet['nombre'] == 's':
                personne = 2
            else:
                personne = 5
    else:
        if isinstance(sujet, str):
            personne = pronoms_personnels[sujet]
        else:
            if sujet['nombre'] == 's':
                personne = 2
            else:
                personne = 5

    verbe = conjugaison(verbe_infinitif, personne, temps)

    for nature in structure_phrase:
        if nature == 'pp':
            pp = sujet
            if pp == 'je' and verbe[0] in VOWELS and not negatif:
                pp = "j'"
            phrase.append(pp)
            if question and negatif:
                phrase.append(mot_negation)
        elif nature == 'sgn':
            gn = sujet
            for m in gn['contenu']:
                phrase.append(m)
        elif nature == 'cod':
            if cod is None:
                gn = noun_group()
                cod = gn
            else:
                gn = cod
            for m in gn['contenu']:
                phrase.append(m)
        elif nature == 'v' or nature == 'vt':
            if negatif:
                if not verbe[0] in VOWELS:
                    phrase.append('ne')
                else:
                    phrase.append("n'")
                phrase.append(verbe)
                # if not question:
                #     phrase.append(mot_negation)
                phrase.append(mot_negation)
            else:
                phrase.append(verbe)
        elif nature == 'adv':
            adv = random.choice(adverbes) if adv is None else adv
            phrase.append(adv)
        elif nature == 'ccl':
            ccl = complement_lieu() if ccl is None else ccl
            for m in ccl['contenu']:
                phrase.append(m)
        elif nature == ',':
            phrase.append(',')
        elif nature == '?':
            phrase.append('?')
        elif nature == '-':
            if sujet[0] in VOWELS:
                if conjugaison(verbe_infinitif, personne, temps)[-1] in 'dt':
                    phrase.append('-')
                else:
                    phrase.append('-t-')
            else:
                phrase.append('-')
        elif nature == 'Est-ce que':
            phrase.append('Est-ce que')

    return {'contenu': phrase,
            'structure': structure_phrase,
            'temps': temps,
            'question': question,
            'negation': {'negatif': negatif, 'mot': mot_negation},
            'personne': personne,
            'sujet': {'contenu': sujet, 'nature': nature_sujet},
            'verbe': {'conjugue': verbe, 'infinitif': verbe_infinitif, 'transitif': transitif},
            'cod': cod,
            'adv': adv,
            'ccl': ccl}


def finalise_phrase(phrase):
    if phrase[-1] == '?':
        return ' '.join(phrase).replace(' , ', ', ').replace("' ", "'").capitalize().replace(' - ', '-').replace(' -t- ', '-t-')
    else:
        return (' '.join(phrase).replace(' , ', ', ').replace("' ", "'") + '.').capitalize()


phrases = []
if __name__ == '__main__':
    for x in range(0, 100):
        phrase = genere_phrase()['contenu']
        phrases.append(finalise_phrase(phrase))
        print(phrases[-1])
