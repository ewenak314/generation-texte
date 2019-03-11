#! /usr/bin/env python3
import random

# True : verbe transitif 
# False : verbe intransitif
verbes = {'manger': [1, 'mang', True], 
          'courir': [3, 'cour', False],
          'dormir': [3, 'dor', False], 
          'marcher': [1, 'march', False], 
          'faire': [3, 'fai', True],
          'fabriquer': [1, 'fabriqu', True], 
          'rigoler': [1, 'rigol', False], 
          'parler': [1, 'parl', False], 
          'boire': [3, 'boi', True],
          'casser': [1, 'cass', True], 
          'applaudir': [2, 'applaud', True]}
verbes_transitifs = [ k for k, v in verbes.items() if v[2] ]
conjug_3e = { 'boire': ['bois', 'bois', 'boit', 'buvons', 'buvez', 'boivent'],
              'courir': ['cours', 'cours', 'court', 'courons', 'courez', 'courent'],
              'dormir': ['dors', 'dors', 'dort', 'dormons', 'dormez', 'dorment'],
              'faire': ['fais', 'fais', 'fait', 'faisons', 'faites', 'font'] }

noms = {'m':['papier', 'ordinateur', 'mot', 'casse-croûte', 'véhicule', 'métier', 'verre', 'bois', 'boa', 'schtroumpf'], 
        'f':['nourriture', 'couverture', 'arrivée', 'tente', 'voiture', 'nature']}
adjectifs = {'m':['noir', 'bleu', 'beau', 'rigolo', 'bizarre', 'breton', 'lumineux', 'grand', 'transparent', 'énorme', 
                  'schtroumpf'],
            'f':['noire', 'bleue', 'belle', 'rigolote', 'bizarre', 'bretonne', 'lumineuse', 'grande', 'transparente', 
                 'énorme', 'schtroumpf']}
adj_devant_nom = ['beau', 'grand', 'belle', 'grande']
pronoms_personnels = {'je': 0, 'tu': 1, 'il': 2, 'elle': 2, 'nous': 3, 'vous': 4, 'ils': 5, 'elles': 5}
determinants = {'m':['le', 'un', 'mon', 'ce', 'notre', 'votre', 'son', 'ton', 'leur'],
                'f':['la', 'une', 'ma', 'cette', 'notre', 'votre', 'sa', 'ta', 'leur']}
adverbes = ['rapidement', 'bien', 'bruyamment', 'calmement', 'sans effort', 'schtroupfement']
preps_lieu = ['à', 'sur', 'dans']
voyelles = 'aeiouyéèà'
structures_phrase = [['gn', 'v', 'adv'], ['gn', 'v'], ['gn', 'vt', 'gn'], ['gn', 'vt', 'gn', 'adv'],
                     ['adv', ',', 'gn','v'], ['pp', 'v'], ['pp', 'v', 'adv'], ['pp', 'vt', 'gn', 'adv'],
                     ['adv', ',', 'pp', 'vt', 'gn'], ['gn', 'vt', 'gn', 'ccl'], ['pp', 'vt', 'gn', 'adv', 'ccl'], 
                     ['adv', ',', 'gn', 'vt', 'gn', 'ccl']]

def groupe_nominal():
    gn = []
    genre = random.choice(['f', 'm'])
    determinant = random.choice(determinants[genre])
    adj = random.choice(adjectifs[genre])
    nom = random.choice(noms[genre])
    if (nom[0] if not adj in adj_devant_nom else adj[0]) in voyelles:
        if determinant in ('le', 'la'):
            determinant = determinant[:-1] + "'"
        elif determinant in ('ma', 'sa', 'ta'):
            determinant = determinant[:-1] + 'on'
        elif determinant == 'ce':
            determinant = 'cet'

    gn.append(determinant)
    if adj in adj_devant_nom:
        gn.append(adj)
    gn.append(nom)
    if not adj in adj_devant_nom:
        gn.append(adj)
    return gn

def conjugaison(verbe, personne):
    if verbe in conjug_3e:
        return conjug_3e[verbe][personne]
    cara_verbe = verbes[verbe]
    radical = cara_verbe[1]
    groupe = cara_verbe[0]
    conjug_1e = ['e', 'es', 'e', 'ons', 'ez', 'ent']
    conjug_2e = ['is', 'is', 'it', 'issons', 'issez', 'issent']
    if groupe == 1:
        return radical + ('e' if (conjug_1e[personne][0] in ['a', 'o', 'u'] and radical[-1] == 'g') else '') + conjug_1e[personne]
    elif groupe == 2:
        return radical + conjug_2e[personne]
    return '[{}]'.format(verbe)

def ccl():
    prep = random.choice(preps_lieu)
    return [prep] + groupe_nominal()

def genere_phrase():
    phrase = []
    structure_phrase = random.choice(structures_phrase)
    personne = 2
    for nature in structure_phrase:
        if nature == 'pp':
            pp = random.choice(list(pronoms_personnels.keys()))
            phrase.append(pp)
            personne = pronoms_personnels[pp]
        if nature == 'gn': 
            for m in groupe_nominal():
                phrase.append(m)
        elif nature == 'v':
            verbe_infinitif = random.choice(list(verbes.keys()))
            phrase.append(conjugaison(verbe_infinitif, personne))
        elif nature == 'vt':
            verbe_infinitif = random.choice(list(verbes_transitifs))
            phrase.append(conjugaison(verbe_infinitif, personne))
        elif nature == 'adv':
            phrase.append(random.choice(adverbes))
        elif nature == 'ccl':
            for m in ccl():
                phrase.append(m)
        elif nature == ',':
            phrase.append(',')
    
    return phrase

if __name__ == '__main__':
    for x in range(0, 100):
        print((' '.join(genere_phrase()).capitalize() + '.').replace(' , ', ', '))