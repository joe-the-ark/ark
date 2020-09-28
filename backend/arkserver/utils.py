avatar_dict = {
    0: 'anteater.svg',
    1: 'bear.svg',
    2: 'boar.svg',
    3: 'beaver.svg',
    4: 'buffalo-1.svg',
    5: 'buffalo.svg',
    6: 'cat.svg',
    7: 'chicken.svg',
    8: 'cow.svg',
    9: 'crow.svg',
    10: 'dog-1.svg',
    11: 'dog.svg',
    12: 'donkey.svg',
    13: 'elephant.svg',
    14: 'fox.svg',
    15: 'giraffe.svg',
    16: 'hedgehog.svg',
    17: 'hen.svg',
    18: 'hippopotamus.svg',
    19: 'horse.svg',
    20: 'kangaroo.svg',
    21: 'koala.svg',
    22: 'leopard.svg',
    23: 'lion.svg',
    24: 'marten.svg',
    25: 'monkey-1.svg',
    26: 'monkey.svg',
    27: 'mouse.svg',
    28: 'octopus.svg',
    29: 'ostrich.svg',
    30: 'owl.svg',
    31: 'panda.svg',
    32: 'parrot.svg',
    33: 'penguin-1.svg',
}

def get_avatar_link(digit):
    from django.contrib.staticfiles.templatetags.staticfiles import static
    name = avatar_dict[int(digit)]
    avatar = static(f'images/avatars/{name}')
    return avatar
    

def list2int(input_list):
    if input_list[0] == '':
        return []
    result = []
    uu = 0
    while uu < len(input_list):
        result.append(int(input_list[uu]))
        uu += 1
    return result

ubung_1_term_list = [
                {
                    'state': 'tag',
                    'value': 'Aufmüpfigkeit',
                    'player_id': -1,
                },
                {
                    'state': 'tag',
                    'value': 'Autonomie',
                    'player_id': -1,
                },
                {
                    'state': 'tag',
                    'value': 'Dominanz',
                    'player_id': -1,
                },
                {
                    'state': 'tag',
                    'value': 'Effizienz',
                    'player_id': -1,
                },
                {
                    'state': 'tag',
                    'value': 'Ehrgeiz',
                    'player_id': -1,
                },
                {
                    'state': 'tag',
                    'value': 'Einzigartigkeit',
                    'player_id': -1,
                },
                {
                    'state': 'tag',
                    'value': 'Erfolg',
                    'player_id': -1,
                },
                {
                    'state': 'tag',
                    'value': 'Flexibilität',
                    'player_id': -1,
                },
                {
                    'state': 'tag',
                    'value': 'Freundschaft',
                    'player_id': -1,
                },
                {
                    'state': 'tag',
                    'value': 'Gelassenheit',
                    'player_id': -1,
                },
                {
                    'state': 'tag',
                    'value': 'Gerechtigkeit',
                    'player_id': -1,
                },
                {
                    'state': 'tag',
                    'value': 'Geselligkeit',
                    'player_id': -1,
                },
                {
                    'state': 'tag',
                    'value': 'Gleichberechtigung',
                    'player_id': -1,
                },
                {
                    'state': 'tag',
                    'value': 'Großzügigkeit',
                    'player_id': -1,
                },
                {
                    'state': 'tag',
                    'value': 'Imagination',
                    'player_id': -1,
                },
                {
                    'state': 'tag',
                    'value': 'Leidenschaft',
                    'player_id': -1,
                },
                {
                    'state': 'tag',
                    'value': 'Loyalität',
                    'player_id': -1,
                },
                {
                    'state': 'tag',
                    'value': 'Mut',
                    'player_id': -1,
                },
                {
                    'state': 'tag',
                    'value': 'Nachhaltigkeit',
                    'player_id': -1,
                },
                {
                    'state': 'tag',
                    'value': 'Neugier',
                    'player_id': -1,
                },
                {
                    'state': 'tag',
                    'value': 'Offenheit',
                    'player_id': -1,
                },
                {
                    'state': 'tag',
                    'value': 'Sicherheit',
                    'player_id': -1,
                },
                {
                    'state': 'tag',
                    'value': 'Sinnhaftigkeit',
                    'player_id': -1,
                },
                {
                    'state': 'tag',
                    'value': 'Solidarität',
                    'player_id': -1,
                },
                {
                    'state': 'tag',
                    'value': 'Sorgfalt',
                    'player_id': -1,
                },
                {
                    'state': 'tag',
                    'value': 'Vergnügen',
                    'player_id': -1,
                },
                {
                    'state': 'tag',
                    'value': 'Vertrautheit',
                    'player_id': -1,
                },
                {
                    'state': 'tag',
                    'value': 'Würde',
                    'player_id': -1,
                },
                {
                    'state': 'tag',
                    'value': 'Zuverlässigkeit',
                    'player_id': -1,
                },
            ]
            

ubung_3_term_list = [
            {
                'state': 'tag',
                'value': 'Abhängigkeit',
                'player_id': -1,
            },
            {
                'state': 'tag',
                'value': 'Achtlosigkeit',
                'player_id': -1,
            },
            {
                'state': 'tag',
                'value': 'Angepasstheit',
                'player_id': -1,
            },
            {
                'state': 'tag',
                'value': 'Angsẗ',
                'player_id': -1,
            },
            {
                'state': 'tag',
                'value': 'Aufgeregtheit',
                'player_id': -1,
            },
            {
                'state': 'tag',
                'value': 'Desinteresse',
                'player_id': -1,
            },
            {
                'state': 'tag',
                'value': 'Distanz',
                'player_id': -1,
            },
            {
                'state': 'tag',
                'value': 'Egoismus',
                'player_id': -1,
            },
            {
                'state': 'tag',
                'value': 'Ehrlosigkeit',
                'player_id': -1,
            },
            {
                'state': 'tag',
                'value': 'Einfallslosigkeit',
                'player_id': -1,
            },
            {
                'state': 'tag',
                'value': 'Feindseligkeit',
                'player_id': -1,
            },
            {
                'state': 'tag',
                'value': 'Gehorsam',
                'player_id': -1,
            },
            {
                'state': 'tag',
                'value': 'Gleichgültigkeit',
                'player_id': -1,
            },
            {
                'state': 'tag',
                'value': 'Leistungsschwäche',
                'player_id': -1,
            },
            {
                'state': 'tag',
                'value': 'Müßiggang',
                'player_id': -1,
            },
            {
                'state': 'tag',
                'value': 'Neid',
                'player_id': -1,
            },
            {
                'state': 'tag',
                'value': 'Rangordnung',
                'player_id': -1,
            },
            {
                'state': 'tag',
                'value': 'Rechthaberei',
                'player_id': -1,
            },
            {
                'state': 'tag',
                'value': 'Risiko',
                'player_id': -1,
            },
            {
                'state': 'tag',
                'value': 'Sinnlosigkeit',
                'player_id': -1,
            },
            {
                'state': 'tag',
                'value': 'Starrheit',
                'player_id': -1,
            },
            {
                'state': 'tag',
                'value': 'Treulosigkeit',
                'player_id': -1,
            },
            {
                'state': 'tag',
                'value': 'Unachtsamkeit',
                'player_id': -1,
            },
            {
                'state': 'tag',
                'value': 'Unterordnung',
                'player_id': -1,
            },
            {
                'state': 'tag',
                'value': 'Unzuverlässigkeit',
                'player_id': -1,
            },
            {
                'state': 'tag',
                'value': 'Verbot',
                'player_id': -1,
            },
            {
                'state': 'tag',
                'value': 'Verkrampftheit',
                'player_id': -1,
            },
            {
                'state': 'tag',
                'value': 'Versagen',
                'player_id': -1,
            },
            {
                'state': 'tag',
                'value': 'Willkür',
                'player_id': -1,
            }]