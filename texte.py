#! /usr/bin/env python3
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

# allows `def func(self, arg: Class)` inside of Class
from __future__ import annotations

import dataclasses
from dataclasses import dataclass
from enum import Enum, auto
import random
import re
import typing


VOWELS = 'aeiouyéèà'


class Chunk:
    def match_to_following_chunk(self, chunk: Chunk):
        return self.match_to_following_string(str(chunk))

    def match_to_following_string(self, string):
        return f'{self} '


class Genre(Enum):
    FEMININE = auto()
    MASCULINE = auto()


class Number(Enum):
    SINGULAR = auto()
    PLURAL = auto()


class Person(Enum):
    FIRST_PERSON = 0
    SECOND_PERSON = 1
    THIRD_PERSON = 2


class Tense(Enum):
    INFINITIVE = auto()
    PAST_PARTICIPLE = auto()
    INDICATIVE_PRESENT = auto()
    INDICATIVE_COMPOUND_PAST = auto()
    INDICATIVE_IMPERFECT = auto()


@dataclass
class Word(Chunk):
    string: str

    def __str__(self):
        return self.string


class PluralMixin:
    als_plurals_list = ['aval', 'bal', 'banal', 'bancal', 'cal', 'carnaval',
                        'cérémonial', 'choral', 'étal', 'fatal', 'festival',
                        'natal', 'naval', 'récital', 'régal', 'tonal', 'pal',
                        'val', 'virginal']
    aux_plurals_list = ['bail', 'corail', 'émail', 'gemmail', 'soupirail',
                        'travail', 'vantail', 'vitrail']
    eus_aus_plurals_list = ['bleu', 'émeu', 'landau', 'lieu', 'pneu', 'sarrau']
    oux_plurals_list = ['bijou', 'caillou', 'chou', 'genou', 'hibou', 'joujou',
                        'pou']

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
        '''This function takes a singular adjective or noun as input and
        returns it in plural'''
        if self.string[-1] in 'szx':
            plural_string = self.string
        elif ((self.string[-2:] in ['au', 'eu'] or self.oux_plural)
              and not self.eus_aus_plural):
            plural_string = self.string + 'x'
        elif self.string[-2:] == 'al' and not self.als_plural:
            plural_string = self.string[:-2] + 'aux'
        elif self.aux_plural:
            plural_string = self.string[:-3] + 'aux'
        else:
            plural_string = self.string + 's'
        return dataclasses.replace(self, string=plural_string,
                                   number=Number.PLURAL)


@dataclass
class Noun(Word, PluralMixin):
    genre: Genre
    number: Number


@dataclass
class Specifier(Word):
    genre: Genre
    number: Number

    _modified_before_vowels_list = {
        'le': "l'", 'la': "l'", 'ma': 'mon ', 'sa': 'son ', 'ta': 'ton ',
        'ce': 'cet ',
    }

    def match_to_following_string(self, string: str) -> str:
        if (string[0] in VOWELS
            and self.string in self._modified_before_vowels_list):
            return self._modified_before_vowels_list[self.string]
        return super().match_to_following_string(string)


@dataclass
class Pronoun(Word):
    genre: Genre | None
    number: Number
    person: Person

    _pronoun_data: typing.ClassVar = {}

    @classmethod
    def register_pronouns(cls, pronouns):
        for p in pronouns:
            cls._pronoun_data[p.string] = p

    def __new__(cls, string=None, genre=None, number=None, person=None):
        if cls is not Pronoun:
            if not getattr(cls, '_instances', None):
                cls._instances = []
            if string is None:
                for instance in cls._instances:
                    if ((instance.genre is None or instance.genre == genre)
                        and instance.number == number and instance.person == person):
                        return instance
                else:
                    raise ValueError(f"Couldn't find any pronoun matching the genre, number and person you specified")
            obj = object.__new__(cls)
            cls._instances.append(obj)
            return obj
        if string is None:
            raise TypeError("Can't create a pronoun without string in base pronoun class. Use a subclass.")
        p = cls._pronoun_data.get(string)
        if p is None:
            raise ValueError(f"Unknown pronoun {string}. Build it with the correct pronoun subclass")
        return p

    def __init__(self, string=None, genre=None, number=None, person=None):
        if getattr(self, '_init_done', False):
            # We're just getting init'ed again after having been found through Pronoun._pronouns_data
            return
        self._init_done = True
        if not all(a is not None for a in (number, person)):
            raise TypeError("Only a pronoun's genre and string may be None")
        self.string = string
        self.genre = genre
        self.number = number
        self.person = person

    @classmethod
    def random(cls, genre, number, person):
        if cls is Pronoun:
            raise
        return cls(genre=genre, number=number, person=person)


class SubjectPronoun(Pronoun):
    pass


SubjectPronoun.register_pronouns((
    SubjectPronoun('je', None, Number.SINGULAR, Person.FIRST_PERSON),
    SubjectPronoun('tu', None, Number.SINGULAR, Person.SECOND_PERSON),
    SubjectPronoun('il', Genre.MASCULINE, Number.SINGULAR, Person.THIRD_PERSON),
    SubjectPronoun('elle', Genre.FEMININE, Number.SINGULAR, Person.THIRD_PERSON),
    SubjectPronoun('on', None, Number.SINGULAR, Person.THIRD_PERSON),
    SubjectPronoun('nous', None, Number.PLURAL, Person.FIRST_PERSON),
    SubjectPronoun('vous', None, Number.PLURAL, Person.SECOND_PERSON),
    SubjectPronoun('ils', Genre.MASCULINE, Number.PLURAL, Person.THIRD_PERSON),
    SubjectPronoun('elles', Genre.FEMININE, Number.PLURAL, Person.THIRD_PERSON),
))


@dataclass
class Adjective(Word, PluralMixin):
    genre: Genre
    number: Number

    _modified_before_vowels_list: typing.ClassVar = {
        'beau': 'bel ', 'nouveau': 'nouvel ', 'vieux': 'vieil '
    }
    _before_noun_list: typing.ClassVar = ['beau', 'grand', 'belle', 'grande']

    @property
    def before_noun(self):
        return self.string in self._before_noun_list

    def match_to_following_string(self, string: str) -> str:
        if string[0] in VOWELS and self.string in self._modified_before_vowels_list:
            return self._modified_before_vowels_list[self.string]
        return super().match_to_following_string(string)


@dataclass
class VerbalBase:
    infinitive: str
    group: int | None = None
    root: str | None = None
    transitive: bool = False
    reflexive: bool = False
    auxiliary: VerbalBase | None = None
    conjugations: dict[Tense, dict[Person, str]] | None = None

    _regular_conjugations: typing.ClassVar = {
        Tense.INDICATIVE_PRESENT: {
            1: ['e', 'es', 'e', 'ons', 'ez', 'ent'],
            2: ['is', 'is', 'it', 'issons', 'issez', 'issent']
        },
        Tense.INDICATIVE_IMPERFECT: {
            1: ['ais', 'ais', 'ait', 'ions', 'iez', 'aient'],
            2: ['issais', 'issais', 'issait', 'issions', 'issiez', 'issaient']
        },
        Tense.PAST_PARTICIPLE: {
            1: {None: 'é'},
            2: {None: 'i'},
        },
    }
    _auxiliaries: typing.ClassVar[dict[str, VerbalBase]] = {}

    def __post_init__(self):
        if self.group is None:
            self.group = 1
            if self.infinitive.endswith('ir'):
                self.group = 2
        if self.root is None:
            m = re.search(r'(.+)[ei]r$', self.infinitive)
            if m is not None:
                self.root = m.group(1)
            else:
                self.root = self.infinitive
        if self.group == 3 and self.conjugations is None:
            raise ValueError(
                "{self}: self.group = 3 but self.conjugations is None")
        if self.auxiliary is None:
            if self.infinitive in ('avoir', 'être'):
                if self.infinitive not in self._auxiliaries:
                    self._auxiliaries[self.infinitive] = self
                self.auxiliary = self._auxiliaries['avoir']
            elif self.reflexive:
                self.auxiliary = self._auxiliaries['être']
            else:
                self.auxiliary = self._auxiliaries['avoir']

    def conjugate(self, tense: Tense, person: Person | None,
                  number: Number = Number.SINGULAR):
        # TODO: reflexive verbs
        if tense in (Tense.INFINITIVE, Tense.PAST_PARTICIPLE):
            person_key = None
        else:
            person_key = person.value
            if number == Number.PLURAL:
                person_key += 3

        if tense == Tense.INFINITIVE:
            return self.infinitive
        elif tense == Tense.INDICATIVE_COMPOUND_PAST:
            aux = self.auxiliary.conjugate(
                Tense.INDICATIVE_PRESENT, person, number)
            participle = self.conjugate(Tense.PAST_PARTICIPLE, None)
            return f'{aux} {participle}'
        elif self.group == 3:
            return self.conjugations[tense][person_key]
        else:
            ending = self._regular_conjugations[tense][self.group][person_key]
            return f'{self.root}{ending}'

avoir_base = VerbalBase(
    'avoir',
    group=3,
    root='',
    transitive=True,
    reflexive=False,
    conjugations={
        Tense.INDICATIVE_PRESENT: ['ai', 'as', 'a', 'avons', 'avez', 'ont'],
        Tense.INDICATIVE_IMPERFECT: [
            'avais', 'avais', 'avait', 'avions', 'aviez', 'avaient'],
        Tense.PAST_PARTICIPLE: {None: 'eu'},
    },
)
etre_base = VerbalBase(
    'être',
    group=3,
    root='',
    transitive=True,
    reflexive=False,
    conjugations={
        Tense.INDICATIVE_PRESENT: [
            'suis', 'es', 'est', 'sommes', 'êtes', 'sont'],
        Tense.INDICATIVE_IMPERFECT: [
            'étais', 'étais', 'était', 'étions', 'étiez', 'étaient'],
        Tense.PAST_PARTICIPLE: {None: 'été'},
    },
)


@dataclass
class Verb(Chunk):
    base: VerbalBase
    tense: Tense
    person: Person | None = None
    number: Number | None = None
    string: str = None

    def __post_init__(self):
        self.string = self.base.conjugate(self.tense, self.person, self.number)

    def __str__(self):
        return self.string



@dataclass
class ChunkGroup(Chunk):
    chunks: list[Chunk]

    def match_to_following_chunk(self, chunk=None):
        iterator = iter(self.chunks[::-1])
        word_list = []
        if chunk is None:
            prev_chunk = next(iterator)
            word_list.append(str(prev_chunk))
        else:
            prev_chunk = chunk

        for word in iterator:
            word_list.append(word.match_to_following_chunk(prev_chunk))
            prev_chunk = word

        return ''.join(word_list[::-1])

    def __str__(self):
        return self.match_to_following_chunk(None)


class WordGroup(ChunkGroup):
    @property
    def words(self):
        return self.chunks

    @words.setter
    def words(self, value):
        self.chunks = value


@dataclass
class NounGroup(WordGroup):
    number: Number = None
    genre: Genre = None
    specifier: Specifier = None
    noun: Noun = None
    adjectives: list[Adjective] = None

    def __init__(self, number=None, genre=None, specifier=None, noun=None,
                 adjectives=None):
        if adjectives is None:
            adjectives = []
        # Genre detection
        if genre is None:
            genre = next((
                w.genre for w in [specifier, noun, *adjectives]
                if w is not None
            ), None)
            if genre is None:
                genre = random.choice(list(Genre))
        else:
            self.genre = genre

        if number is None:
            number = next((
                w.number for w in [specifier, noun, *adjectives]
                if w is not None
            ), None)
            if number is None:
                number = random.choice(list(Number))
        else:
            self.number = number

        if specifier is None:
            self.specifier = Specifier(
                random.choice(
                    determinants[genre]) if number == Number.SINGULAR
                    else random.choice(determinants[number]
                ),
                genre=genre, number=number)
        else:
            self.specifier = specifier

        if not adjectives:
            self.adjectives = [Adjective(random.choice(adjectifs[genre]),
                                         genre=genre, number=number)]
        else:
            self.adjectives = adjectives

        if noun is None:
            self.noun = Noun(random.choice(noms[genre]), genre=genre,
                             number=number)
        else:
            self.noun = noun

        if number == Number.PLURAL:
            self.adjectives = [adj.plural() for adj in adjectives]
            self.noun = self.noun.plural()

        self.words = [
            self.specifier,
            *(adj for adj in self.adjectives if adj.before_noun),
            self.noun,
            *(adj for adj in self.adjectives if not adj.before_noun)]

    @classmethod
    def random(cls, **kwargs):
        return cls(number=kwargs.get('number'), genre=kwargs.get('genre'))


class FunctionWordGroup(WordGroup):
    def __init__(self, chunk=None, **kwargs):
        if chunk is None:
            chunk = random.choice(self.DEFAULT_CHUNK_TYPES)

        if isinstance(chunk, Chunk):
            self.chunks = [chunk]
        else:
            if set(kwargs.keys()) != self.ARGS:
                raise TypeError(f"Exactly the following arguments should be passed to {self.__class__}: {self.ARGS}")
            self.chunks = [chunk.random(**kwargs)]


class DirectObject(FunctionWordGroup):
    DEFAULT_CHUNK_TYPES = (NounGroup,)
    ARGS = {'genre', 'number'}


class Subject(FunctionWordGroup):
    DEFAULT_CHUNK_TYPES = (NounGroup, SubjectPronoun)
    ARGS = {'genre', 'number', 'person'}


class Sentence(ChunkGroup):
    pass


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


def convert_conjugations(conjugations):
    return {
        Tense.INDICATIVE_PRESENT: conjugations['indicatif']['present'],
        Tense.INDICATIVE_IMPERFECT: conjugations['indicatif']['imparfait'],
        Tense.PAST_PARTICIPLE: {None: conjugations['participe']['passe']},
    }


def conjugaison(verbe, personne=None, temps='present', *,
                ajouter_pronoms=True):
    '''Conjugue le verbe passé en paramètre
    au temps et à la personne voulus'''
    if personne is None and temps != 'participe_passe':
        return verbe
    verbe_conjugue = []
    if isinstance(verbe, dict):
        cara_verbe = verbe
    elif verbe in verbes:
        cara_verbe = verbes[verbe]
    else:
        m = re.search(r'(.+)([ei]r)$', verbe)
        if m is not None:
            radical, terminaison = m.groups()
            groupe = 1 if terminaison == 'er' else 2
        else:
            return verbe
        cara_verbe = {'groupe': groupe, 'radical': radical, 'transitif': False,
                      'pronominal': False}
    radical = cara_verbe['radical']
    groupe = cara_verbe['groupe']
    if groupe != 3:
        conjugations = None
    elif isinstance(verbe, dict) and 'conjugaisons' in verbe:
        conjugations = convert_conjugations(verbe)
    elif verbe in conjug_3e:
        conjugations = convert_conjugations(conjug_3e[verbe])
    tense = {
        'present': Tense.INDICATIVE_PRESENT,
        'imparfait': Tense.INDICATIVE_IMPERFECT,
        'passe_compose': Tense.INDICATIVE_COMPOUND_PAST,
    }[temps]
    if isinstance(personne, Person):
        number = Number.SINGULAR
        person = personne
    elif personne >= 3:
        number = Number.PLURAL
        person = Person(personne - 3)
    else:
        number = Number.SINGULAR
        person = Person(personne)

    base = VerbalBase(
        verbe if not isinstance(verbe, dict) else (
            radical + 'ir' if groupe == 2 else radical + 'er'),
        group=groupe, root=radical, transitive=cara_verbe['transitif'],
        reflexive=cara_verbe['pronominal'], conjugations=conjugations
    )
    return base.conjugate(tense, person, number)

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
        elif isinstance(verbe, dict):
            verbe_conjugue = verbe['conjugaisons']['indicatif'][temps][personne]
        else:
            verbe_conjugue = conjug_3e[verbe]['indicatif'][temps][personne]
    elif temps == 'participe_passe':
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
            if verbe_conjugue[0] not in VOWELS or pronoms_personnels_reflechis[personne][-1] not in VOWELS:
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
    complement = [prep] + gn.words
    return {'contenu': complement, 'prep': prep, 'cod': gn}


def genere_phrase(structure=None, temps=None, question=None, negatif=None, mot_negation=None, sujet=None, verbe=None, cod=None, adv=None, ccl=None):
    'Génère une phrase'
    phrase = []
    pas_de_structure = all(var is None for var in (structure, sujet, verbe, cod,
                                                   adv, ccl))
    if pas_de_structure:
        structure_phrase = random.choice(structures_phrase)
    elif structure is not None:
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
        elif transitif:
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
        verbe_infinitif = (random.choice([v for v in verbes if v not in ('être', 'avoir')]) if 'v' in structure_phrase
                           else random.choice(verbes_transitifs))
    else:
        verbe_infinitif = verbe
        if not isinstance(verbe, dict) and verbe not in verbes:
            print(f"""Ce programme ne connais pas le verbe {verbe}. \
Il est possible de passer un dictionnaire en paramètre avec les champs \
infinitif (str), groupe (int), radical (str), transitif (bool) et pronominal (bool) et aussi, \
si le verbe est du troisième groupe, conjugaisons (list).""")
            return None

    nature_sujet = 'pp' if 'pp' in structures_phrase else 'gn'

    # Définition de la personne
    if sujet is None:
        if nature_sujet == 'pp':
            sujet = random.choice(list(pronoms_personnels.keys()))
            personne = pronoms_personnels[sujet]
        else:
            sujet = NounGroup()
            personne = Person.THIRD_PERSON
    elif isinstance(sujet, str):
        personne = pronoms_personnels[sujet]
    else:
        personne = 2 if sujet['nombre'] == 's' else 5

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
            phrase.extend(gn['contenu'])
        elif nature == 'cod':
            if cod is None:
                gn = noun_group()
                cod = gn
            else:
                gn = cod
            phrase.extend(gn['contenu'])
        elif nature in ('v', 'vt'):
            if negatif:
                if verbe[0] not in VOWELS:
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
            phrase.extend(ccl['contenu'])
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
    for _ in range(0, 100):
        phrase = genere_phrase()['contenu']
        phrases.append(finalise_phrase(phrase))
        print(phrases[-1])
