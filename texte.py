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

import random

#Données

# True : verbe transitif
# False : verbe intransitif
verbes = {'manger': {'groupe': 1, 'radical': 'mang', 'transitif': True},
          'courir': {'groupe': 3, 'radical': 'cour', 'transitif': False},
          'dormir': {'groupe': 3, 'radical': 'dor', 'transitif': False},
          'marcher': {'groupe': 1, 'radical': 'march', 'transitif': False},
          'faire': {'groupe': 3, 'radical': 'fai','transitif': True},
          'fabriquer': {'groupe': 1, 'radical': 'fabriqu', 'transitif': True},
          'rigoler': {'groupe': 1, 'radical': 'rigol', 'transitif': False},
          'parler': {'groupe': 1, 'radical': 'parl', 'transitif': False},
          'boire': {'groupe': 3, 'radical': 'boi', 'transitif': True},
          'casser': {'groupe': 1, 'radical': 'cass', 'transitif': True},
          'applaudir': {'groupe': 2, 'radical': 'applaud', 'transitif': True},
          'être': {'groupe': 3, 'radical': '', 'transitif': True},
          'sculpter': {'groupe': 1, 'radical': 'sculpt', 'transitif': True},
          'prendre': {'groupe': 3, 'radical': 'prend', 'transitif': True},
          'souvenir': {'groupe': 3, 'radical': 'souv', 'transitif': True},
          'avoir': {'groupe': 3, 'radical': '', 'transitif': True},
          'enclencher': {'groupe': 1, 'radical': 'enclench', 'transitif': True}}
verbes_transitifs = [ k for k, v in verbes.items() if v['transitif'] ]
conjugaisons = {
    'indicatif': {
        'présent' : {
            1: ['e', 'es', 'e', 'ons', 'ez', 'ent'],
            2: ['is', 'is', 'it', 'issons', 'issez', 'issent']
        },
        'imparfait': {
            1: ['ais', 'ais', 'ait', 'ions', 'iez', 'aient'],
            2: ['issais', 'issais', 'issait', 'issions', 'issiez', 'issaient']
        }
    }
}
conjug_3e = { 'boire': ['bois', 'bois', 'boit', 'buvons', 'buvez', 'boivent'],
              'courir': ['cours', 'cours', 'court', 'courons', 'courez', 'courent'],
              'dormir': ['dors', 'dors', 'dort', 'dormons', 'dormez', 'dorment'],
              'faire': ['fais', 'fais', 'fait', 'faisons', 'faites', 'font'],
              'être': ['suis', 'es', 'est', 'sommes', 'êtes', 'sont'],
              'prendre': ['prends', 'prends', 'prend', 'prenons', 'prenez', 'prennent'],
              'souvenir': ['souviens', 'souviens', 'souviens', 'souvenons', 'souvenez', 'souviennent'],
              'avoir': ['ai', 'as', 'a', 'avons', 'avez', 'ont']}

noms = {'m': ['papier', 'ordinateur', 'mot', 'casse-croûte', 'véhicule', 'métier', 'verre', 'bois', 'boa', 'schtroumpf',
              'remède', 'zéro', 'masseur', 'lit', 'pneu', 'jeu'],
        'f': ['nourriture', 'couverture', 'arrivée', 'tente', 'voiture', 'nature', 'masseur', 'discussion', 'éternité',
              'bonté']}
adjectifs = {'m':['noir', 'bleu', 'beau', 'rigolo', 'bizarre', 'breton', 'lumineux', 'grand', 'transparent', 'énorme',
                  'schtroumpf', 'sage', 'embêtant', 'faible', 'fainéant', 'grossier'],
            'f':['noire', 'bleue', 'belle', 'rigolote', 'bizarre', 'bretonne', 'lumineuse', 'grande', 'transparente',
                 'énorme', 'schtroumpf', 'sage', 'embêtante', 'faible', 'fainéante', 'grossière']}
adjectifs_devant_nom = ['beau', 'grand', 'belle', 'grande']
adj_changeant_radical_voyelles = {'beau': 'bel', 'nouveau': 'nouvel', 'vieux': 'vieil'}
pronoms_personnels = {'je': 0, 'tu': 1, 'il': 2, 'elle': 2, 'nous': 3, 'vous': 4, 'ils': 5, 'elles': 5}
determinants = {'m':['le', 'un', 'mon', 'ce', 'notre', 'votre', 'son', 'ton', 'leur', 'quelque'],
                'f':['la', 'une', 'ma', 'cette', 'notre', 'votre', 'sa', 'ta', 'leur', 'quelque'],
                'pl':['les', 'des', 'mes', 'ces', 'nos', 'vos', 'ses', 'tes', 'leurs', 'quelques']}
adverbes = ['rapidement', 'bien', 'bruyamment', 'calmement', 'sans effort', 'schtroumpfement', 'jeunement',
            'perpétuellement', 'fatalement', 'épisodiquement', 'farouchement', 'intégralement',
            'individuellement', 'anticonstitutionnellement']
prepositions_lieu = ['à', 'sur', 'dans']
voyelles = 'aeiouyéèà'
structures_phrase = [['sgn', 'v', 'adv'], ['sgn', 'v'], ['sgn', 'vt', 'cod'], ['sgn', 'vt', 'cod', 'adv'],
                     ['adv', ',', 'sgn','v'], ['pp', 'v'], ['pp', 'v', 'adv'], ['pp', 'vt', 'cod', 'adv'],
                     ['adv', ',', 'pp', 'vt', 'cod'], ['sgn', 'vt', 'cod', 'ccl'], ['pp', 'vt', 'cod', 'adv', 'ccl'],
                     ['adv', ',', 'sgn', 'vt', 'cod', 'ccl']]
pluriel_en_als = ['aval', 'bal', 'banal', 'bancal', 'cal', 'carnaval', 'cérémonial', 'choral', 'étal', 'fatal', 'festival',
             'natal', 'naval', 'récital', 'régal', 'tonal', 'pal', 'val', 'virginal']
pluriel_en_aux = ['bail', 'corail', 'émail', 'gemmail', 'soupirail', 'travail', 'vantail', 'vitrail']
pluriel_en_eus_aus = ['bleu', 'émeu', 'landau', 'lieu', 'pneu', 'sarrau']
pluriel_en_oux = ['bijou', 'caillou', 'chou', 'genou', 'hibou', 'joujou', 'pou']

class EmptyRootError(NameError):
    pass

def pluriel(mot):
    '''La fonction pluriel prend en paramètre
    un adjectif ou un nom et le renvoie au pluriel'''
    if mot[-1] in 'szx':
        return mot
    elif (mot[-2:] in ['au', 'eu'] or mot in pluriel_en_oux) and (not mot in pluriel_en_eus_aus):
        return mot + 'x'
    elif mot[-2:] == 'al' and not mot in pluriel_en_als:
        return mot[:-2] + 'aux'
    elif mot in pluriel_en_aux:
        return mot[:-3] + 'aux'
    else:
        return mot + 's'

pluriels = dict([ (m, pluriel(m)) for m in noms['m'] + noms['f'] + adjectifs['m'] + adjectifs['f'] if pluriel(m) != m ] +
                 [ (determinants['m'][i], determinants['pl'][i]) for i in range(0, len(determinants['m']))])

def groupe_nominal(det=None, nom=None, adj=None, genre=None, nombre=None):
    '''Renvoie un groupe nominal (gn) dont
    on peut spécifier certaines choses'''
    gn = []
    #Genre
    if genre is None:
        if det is not None and not det in determinants['pl']:
            genre = 'm' if det in determinants['m'] else 'f'
        elif nom is not None:
            if nom in noms['m'] or nom in [pluriel(n) for n in noms['m']]:
                genre = 'm'
            else:
                genre = 'f'
        elif adj is not None:
            if adj in adjectifs['m'] or adj in [pluriel(m) for m in adjectifs['m']]:
                genre = 'm'
            else:
                genre = 'f'
        else:
            genre = random.choice(['m', 'f'])

    if nombre is None:
        if det is None and adj is None and nom is None:
            nombre = random.choice(['s', 'p'])
        else:
            nombre = 's' if not (det in pluriels.values() or nom in pluriels.values() or adj in pluriels.values()) else 'p'
    if det is None:
        det = random.choice(determinants[genre]) if nombre == 's' else random.choice(determinants['pl'])
    if adj is None:
        adj = random.choice(adjectifs[genre])
    if nom is None:
        nom = random.choice(noms[genre])

    adj_devant_nom = adj in adjectifs_devant_nom
    if adj in adj_changeant_radical_voyelles and nom[0] in voyelles and genre == 'm' and nombre == 's':
        adj = adj_changeant_radical_voyelles[adj]

    #Pluriel
    if nombre == 'p':
        adj = pluriel(adj)
        nom = pluriel(nom)

    if adj_devant_nom:
        gn = [det, adj, nom]
    else:
        gn = [det, nom, adj]

    #Correction de l'orthographe du déterminant en fonction du mot qu'il y a après
    if gn[1][0] in voyelles:
        if det in ('le', 'la'):
            gn[0] = "l'"
        elif det in ('ma', 'sa', 'ta'):
            gn[0] = det[:-1] + 'on'
        elif det == 'ce':
            gn[0] = 'cet'

    return {'contenu': gn, 'nombre': nombre, 'genre': genre, 'det': det, 'nom': nom, 'adj': adj}

def conjugaison(verbe, personne, temps='present_indicatif'): # pi = présent indicatif, imp = imparfait (indicatif)
    '''Conjugue le verbe passé en paramètre
    au temps et à la personne voulus'''
    if verbe in verbes:
        if verbes[verbe]['groupe'] == 3:
            return conjug_3e[verbe][personne]
        cara_verbe = verbes[verbe]
        radical = cara_verbe['radical']
        groupe = cara_verbe['groupe']
        terminaison = conjugaisons['indicatif']['présent' if temps == 'present_indicatif' else 'imparfait'][groupe][personne]
        if radical == '':
            raise EmptyRootError(verbe)
        if groupe == 1:
            return radical + ('e' if (terminaison[0] in ['a', 'o', 'u'] and radical[-1] == 'g') else '') + terminaison
        elif groupe == 2:
            return radical + terminaison
    else:
        return verbe

def complement_lieu(prep=None, gn=None):
    'Génère complément circonstanciel de temps'
    if prep is None:
        prep = random.choice(prepositions_lieu)
    if gn is None:
        gn = groupe_nominal()
    if prep == 'à' and gn['contenu'][0] == 'le':
        prep = 'au'
        gn['det'] = ''
        gn['contenu'][0] = ''
    complement = [prep] + gn['contenu']
    return {'contenu': complement, 'prep': prep, 'cod': gn}

def genere_phrase(structure=None, temps=None, question=None, negatif=None, mot_negation=None, sujet=None, verbe=None, cod=None, adv=None, ccl=None):
    'Génère une phrase'
    phrase = []
    if (structure is None and sujet is None
        and verbe is None and cod is None
        and adv is None and ccl is None):
        structure_phrase = random.choice(structures_phrase)
    else:
        if structure is not None:
            structure_phrase = structure
        else:
            contenu_min = []
            if sujet is not None:
                if isinstance(sujet, str):
                    contenu_min.append('pp')
                else:
                    contenu_min.append('sgn')
            if verbe is not None:
                contenu_min.append('v')
            if cod is not None:
                contenu_min.append('cod')
            if adv is not None:
                contenu_min.append('adv')
            if ccl is not None:
                contenu_min.append('ccl')
            contenu_min = set(contenu_min)
            structures_possibles = [ s for s in structures_phrase if contenu_min.difference(set(s)) == set()]
            structure_phrase = random.choice(structures_possibles)

    transitif = 'vt' in structure_phrase

    if temps is None:
        temps = random.choice(['present_indicatif', 'imparfait'])
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
    elif mot_negation is not None and negatif != False:
        negatif = True
    if negatif and mot_negation is None:
        mot_negation = random.choice(['pas', 'plus', 'jamais', 'presque plus', 'presque jamais'])
    personne = 2

    if verbe is None:
        verbe_infinitif = (random.choice([ v for v in verbes.keys() if v != 'être']) if 'v' in structure_phrase
                           else random.choice(verbes_transitifs))
    else:
        if verbe in verbes:
            verbe_infinitif = verbe
        else:
            if isinstance(verbe, dict):
                verbes[verbe['infinitif']] = verbe
                if verbe['groupe'] == 3:
                    conjug_3e[verbe['infinitif']] = verbe['conjugaisons']
                verbe_infinitif = verbe['infinitif']
            else:
                print("""Ce programme ne connais pas le verbe {verbe}. \
Il est possible de passer un dictionnaire en paramètre avec les champs \
infinitif (str), groupe (int), radical (str) et transitif (bool) et aussi, \
si le verbe est du troisième groupe, conjugaisons (list).""")
                verbe_infinitif = verbe

    if 'pp' in structure_phrase:
        nature_sujet = 'pp'
    else:
        nature_sujet = 'gn'

    #Définition de la personne
    if sujet is None:
        if nature_sujet == 'pp':
            sujet = random.choice(list(pronoms_personnels.keys()))
            personne = pronoms_personnels[sujet]
        else:
            sujet = groupe_nominal()
    else:
        if isinstance(sujet, str):
            personne = pronoms_personnels[sujet]
        else:
            if sujet['nombre'] == 's':
                personne = 2
            else:
                personne = 5

    for nature in structure_phrase:
        if nature == 'pp':
            pp = sujet
            if pp == 'je' and verbe_infinitif[0] in voyelles:
                pp = "J'"
            phrase.append(pp)
        elif nature == 'sgn':
            if sujet is None:
                gn = groupe_nominal()
                sujet = gn
            else:
                gn = sujet
            if gn['nombre'] == 'p':
                personne = 5
            for m in gn['contenu']:
                phrase.append(m)
        elif nature == 'cod':
            if cod is None:
                gn = groupe_nominal()
                cod = gn
            else:
                gn = cod
            for m in gn['contenu']:
                phrase.append(m)
        elif nature == 'v':
            verbe = conjugaison(verbe_infinitif, personne, temps)
            if negatif:
                if not verbe[0] in voyelles:
                    phrase.append('ne')
                else:
                    phrase.append("n'")
                phrase.append(verbe)
                phrase.append(mot_negation)
            else:
                phrase.append(verbe)
        elif nature == 'vt':
            verbe = conjugaison(verbe_infinitif, personne, temps)
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
            if sujet[0] in voyelles:
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
