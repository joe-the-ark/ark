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
                    'value': 'Humor',
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
                'value': 'Angst',
                'player_id': -1,
            },
            {
                'state': 'tag',
                'value': 'Aufgeregtheit',
                'player_id': -1,
            },
            {
                'state': 'tag',
                'value': 'Trübsal',
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


ubung_1_term_list_i18n = {
    'Deutsch': [
        {
            'id': 0,
            'state': 'tag',
            'value': 'Autonomie',
            'player_id': -1,
        },
        {
            'id': 1,
            'state': 'tag',
            'value': 'Dominanz',
            'player_id': -1,
        },
        {
            'id': 2,
            'state': 'tag',
            'value': 'Effizienz',
            'player_id': -1,
        },
        {
            'id': 3,
            'state': 'tag',
            'value': 'Ehrgeiz',
            'player_id': -1,
        },
        {
            'id': 4,
            'state': 'tag',
            'value': 'Einzigartigkeit',
            'player_id': -1,
        },
        {
            'id': 5,
            'state': 'tag',
            'value': 'Erfolg',
            'player_id': -1,
        },
        {
            'id': 6,
            'state': 'tag',
            'value': 'Flexibilität',
            'player_id': -1,
        },
        {
            'id': 7,
            'state': 'tag',
            'value': 'Freundschaft',
            'player_id': -1,
        },
        {
            'id': 8,
            'state': 'tag',
            'value': 'Gelassenheit',
            'player_id': -1,
        },
        {
            'id': 9,
            'state': 'tag',
            'value': 'Gerechtigkeit',
            'player_id': -1,
        },
        {
            'id': 10,
            'state': 'tag',
            'value': 'Geselligkeit',
            'player_id': -1,
        },
        {
            'id': 11,
            'state': 'tag',
            'value': 'Gleichberechtigung',
            'player_id': -1,
        },
        {
            'id': 12,
            'state': 'tag',
            'value': 'Großzügigkeit',
            'player_id': -1,
        },
        {
            'id': 13,
            'state': 'tag',
            'value': 'Humor',
            'player_id': -1,
        },
        {
            'id': 14,
            'state': 'tag',
            'value': 'Imagination',
            'player_id': -1,
        },
        {
            'id': 15,
            'state': 'tag',
            'value': 'Leidenschaft',
            'player_id': -1,
        },
        {
            'id': 16,
            'state': 'tag',
            'value': 'Loyalität',
            'player_id': -1,
        },
        {
            'id': 17,
            'state': 'tag',
            'value': 'Mut',
            'player_id': -1,
        },
        {
            'id': 18,
            'state': 'tag',
            'value': 'Nachhaltigkeit',
            'player_id': -1,
        },
        {
            'id': 19,
            'state': 'tag',
            'value': 'Neugier',
            'player_id': -1,
        },
        {
            'id': 20,
            'state': 'tag',
            'value': 'Offenheit',
            'player_id': -1,
        },
        {
            'id': 21,
            'state': 'tag',
            'value': 'Sicherheit',
            'player_id': -1,
        },
        {
            'id': 22,
            'state': 'tag',
            'value': 'Sinnhaftigkeit',
            'player_id': -1,
        },
        {
            'id': 23,
            'state': 'tag',
            'value': 'Solidarität',
            'player_id': -1,
        },
        {
            'id': 24,
            'state': 'tag',
            'value': 'Sorgfalt',
            'player_id': -1,
        },
        {
            'id': 25,
            'state': 'tag',
            'value': 'Vergnügen',
            'player_id': -1,
        },
        {
            'id': 26,
            'state': 'tag',
            'value': 'Vertrautheit',
            'player_id': -1,
        },
        {
            'id': 27,
            'state': 'tag',
            'value': 'Würde',
            'player_id': -1,
        },
        {
            'id': 28,
            'state': 'tag',
            'value': 'Zuverlässigkeit',
            'player_id': -1,
        },
    ],
    'French': [
        {
            'id': 0,
            'state': 'tag',
            'value': 'autonomie',
            'player_id': -1,
        },
        {
            'id': 1,
            'state': 'tag',
            'value': 'dominance',
            'player_id': -1,
        },
        {
            'id': 2,
            'state': 'tag',
            'value': 'efficacité',
            'player_id': -1,
        },
        {
            'id': 3,
            'state': 'tag',
            'value': 'ambition',
            'player_id': -1,
        },
        {
            'id': 4,
            'state': 'tag',
            'value': 'originalité',
            'player_id': -1,
        },
        {
            'id': 5,
            'state': 'tag',
            'value': 'performance',
            'player_id': -1,
        },
        {
            'id': 6,
            'state': 'tag',
            'value': 'flexibilité',
            'player_id': -1,
        },
        {
            'id': 7,
            'state': 'tag',
            'value': 'amitié',
            'player_id': -1,
        },
        {
            'id': 8,
            'state': 'tag',
            'value': 'calme',
            'player_id': -1,
        },
        {
            'id': 9,
            'state': 'tag',
            'value': 'équité',
            'player_id': -1,
        },
        {
            'id': 10,
            'state': 'tag',
            'value': 'convivialité',
            'player_id': -1,
        },
        {
            'id': 11,
            'state': 'tag',
            'value': 'égalité',
            'player_id': -1,
        },
        {
            'id': 12,
            'state': 'tag',
            'value': 'générosité',
            'player_id': -1,
        },
        {
            'id': 13,
            'state': 'tag',
            'value': 'humour',
            'player_id': -1,
        },
        {
            'id': 14,
            'state': 'tag',
            'value': 'imagination',
            'player_id': -1,
        },
        {
            'id': 15,
            'state': 'tag',
            'value': 'passion',
            'player_id': -1,
        },
        {
            'id': 16,
            'state': 'tag',
            'value': 'fidélité',
            'player_id': -1,
        },
        {
            'id': 17,
            'state': 'tag',
            'value': 'courage',
            'player_id': -1,
        },
        {
            'id': 18,
            'state': 'tag',
            'value': 'durabilité',
            'player_id': -1,
        },
        {
            'id': 19,
            'state': 'tag',
            'value': 'curiosité',
            'player_id': -1,
        },
        {
            'id': 20,
            'state': 'tag',
            'value': 'candeur',
            'player_id': -1,
        },
        {
            'id': 21,
            'state': 'tag',
            'value': 'sécurité',
            'player_id': -1,
        },
        {
            'id': 22,
            'state': 'tag',
            'value': 'sens',
            'player_id': -1,
        },
        {
            'id': 23,
            'state': 'tag',
            'value': 'solidarité',
            'player_id': -1,
        },
        {
            'id': 24,
            'state': 'tag',
            'value': 'prudence',
            'player_id': -1,
        },
        {
            'id': 25,
            'state': 'tag',
            'value': 'plaisir',
            'player_id': -1,
        },
        {
            'id': 26,
            'state': 'tag',
            'value': 'familiarité ',
            'player_id': -1,
        },
        {
            'id': 27,
            'state': 'tag',
            'value': 'dignité',
            'player_id': -1,
        },
        {
            'id': 28,
            'state': 'tag',
            'value': 'fiabilité',
            'player_id': -1,
        },
    ],
    'Chinese': [
        {
            'id': 0,
            'state': 'tag',
            'value': '自治',
            'player_id': -1,
        },
        {
            'id': 1,
            'state': 'tag',
            'value': '优势',
            'player_id': -1,
        },
        {
            'id': 2,
            'state': 'tag',
            'value': '效率',
            'player_id': -1,
        },
        {
            'id': 3,
            'state': 'tag',
            'value': '志向',
            'player_id': -1,
        },
        {
            'id': 4,
            'state': 'tag',
            'value': '独特性',
            'player_id': -1,
        },
        {
            'id': 5,
            'state': 'tag',
            'value': '性能',
            'player_id': -1,
        },
        {
            'id': 6,
            'state': 'tag',
            'value': '弹性',
            'player_id': -1,
        },
        {
            'id': 7,
            'state': 'tag',
            'value': '交情',
            'player_id': -1,
        },
        {
            'id': 8,
            'state': 'tag',
            'value': '沉着',
            'player_id': -1,
        },
        {
            'id': 9,
            'state': 'tag',
            'value': '公平性',
            'player_id': -1,
        },
        {
            'id': 10,
            'state': 'tag',
            'value': '友好关系',
            'player_id': -1,
        },
        {
            'id': 11,
            'state': 'tag',
            'value': '平等',
            'player_id': -1,
        },
        {
            'id': 12,
            'state': 'tag',
            'value': '慷慨',
            'player_id': -1,
        },
        {
            'id': 13,
            'state': 'tag',
            'value': '幽默',
            'player_id': -1,
        },
        {
            'id': 14,
            'state': 'tag',
            'value': '想象力',
            'player_id': -1,
        },
        {
            'id': 15,
            'state': 'tag',
            'value': '激情',
            'player_id': -1,
        },
        {
            'id': 16,
            'state': 'tag',
            'value': '忠诚',
            'player_id': -1,
        },
        {
            'id': 17,
            'state': 'tag',
            'value': '勇气',
            'player_id': -1,
        },
        {
            'id': 18,
            'state': 'tag',
            'value': '可持续',
            'player_id': -1,
        },
        {
            'id': 19,
            'state': 'tag',
            'value': '好奇心',
            'player_id': -1,
        },
        {
            'id': 20,
            'state': 'tag',
            'value': '公开性',
            'player_id': -1,
        },
        {
            'id': 21,
            'state': 'tag',
            'value': '安全',
            'player_id': -1,
        },
        {
            'id': 22,
            'state': 'tag',
            'value': '意义性',
            'player_id': -1,
        },
        {
            'id': 23,
            'state': 'tag',
            'value': '团结',
            'player_id': -1,
        },
        {
            'id': 24,
            'state': 'tag',
            'value': '细心',
            'player_id': -1,
        },
        {
            'id': 25,
            'state': 'tag',
            'value': '乐趣',
            'player_id': -1,
        },
        {
            'id': 26,
            'state': 'tag',
            'value': '熟悉',
            'player_id': -1,
        },
        {
            'id': 27,
            'state': 'tag',
            'value': '尊严',
            'player_id': -1,
        },
        {
            'id': 28,
            'state': 'tag',
            'value': '可靠性',
            'player_id': -1,
        },
    ],
    'Turkish': [
        {'id': 0,  'state': 'tag', 'value': 'özerklik',            'player_id': -1},
        {'id': 1,  'state': 'tag', 'value': 'baskınlık',           'player_id': -1},
        {'id': 2,  'state': 'tag', 'value': 'verimlilik',          'player_id': -1},
        {'id': 3,  'state': 'tag', 'value': 'hırs',                'player_id': -1},
        {'id': 4,  'state': 'tag', 'value': 'benzersizlik',        'player_id': -1},
        {'id': 5,  'state': 'tag', 'value': 'başarı',              'player_id': -1},
        {'id': 6,  'state': 'tag', 'value': 'esneklik',            'player_id': -1},
        {'id': 7,  'state': 'tag', 'value': 'arkadaşlık',          'player_id': -1},
        {'id': 8,  'state': 'tag', 'value': 'sakinlik',            'player_id': -1},
        {'id': 9,  'state': 'tag', 'value': 'adalet',              'player_id': -1},
        {'id': 10, 'state': 'tag', 'value': 'sosyallik',           'player_id': -1},
        {'id': 11, 'state': 'tag', 'value': 'eşitlik',             'player_id': -1},
        {'id': 12, 'state': 'tag', 'value': 'cömertlik',           'player_id': -1},
        {'id': 13, 'state': 'tag', 'value': 'mizah',               'player_id': -1},
        {'id': 14, 'state': 'tag', 'value': 'hayalgücü',          'player_id': -1},
        {'id': 15, 'state': 'tag', 'value': 'tutku',               'player_id': -1},
        {'id': 16, 'state': 'tag', 'value': 'sadakat',             'player_id': -1},
        {'id': 17, 'state': 'tag', 'value': 'cesaret',             'player_id': -1},
        {'id': 18, 'state': 'tag', 'value': 'sürdürülebilirlik',   'player_id': -1},
        {'id': 19, 'state': 'tag', 'value': 'merak',               'player_id': -1},
        {'id': 20, 'state': 'tag', 'value': 'açıklık',             'player_id': -1},
        {'id': 21, 'state': 'tag', 'value': 'güvenlik',            'player_id': -1},
        {'id': 22, 'state': 'tag', 'value': 'anlamlılık',          'player_id': -1},
        {'id': 23, 'state': 'tag', 'value': 'dayanışma',           'player_id': -1},
        {'id': 24, 'state': 'tag', 'value': 'özen',                'player_id': -1},
        {'id': 25, 'state': 'tag', 'value': 'keyif',               'player_id': -1},
        {'id': 26, 'state': 'tag', 'value': 'aşinalık',            'player_id': -1},
        {'id': 27, 'state': 'tag', 'value': 'onur',                'player_id': -1},
        {'id': 28, 'state': 'tag', 'value': 'güvenilirlik',        'player_id': -1},
    ],
    'English': [
        {
            'id': 0,
            'state': 'tag',
            'value': 'autonomy',
            'player_id': -1,
        },
        {
            'id': 1,
            'state': 'tag',
            'value': 'dominance',
            'player_id': -1,
        },
        {
            'id': 2,
            'state': 'tag',
            'value': 'efficiency',
            'player_id': -1,
        },
        {
            'id': 3,
            'state': 'tag',
            'value': 'ambition',
            'player_id': -1,
        },
        {
            'id': 4,
            'state': 'tag',
            'value': 'uniqueness',
            'player_id': -1,
        },
        {
            'id': 5,
            'state': 'tag',
            'value': 'performance',
            'player_id': -1,
        },
        {
            'id': 6,
            'state': 'tag',
            'value': 'flexibility',
            'player_id': -1,
        },
        {
            'id': 7,
            'state': 'tag',
            'value': 'friendship',
            'player_id': -1,
        },
        {
            'id': 8,
            'state': 'tag',
            'value': 'composure',
            'player_id': -1,
        },
        {
            'id': 9,
            'state': 'tag',
            'value': 'fairness',
            'player_id': -1,
        },
        {
            'id': 10,
            'state': 'tag',
            'value': 'conviviality',
            'player_id': -1,
        },
        {
            'id': 11,
            'state': 'tag',
            'value': 'equality',
            'player_id': -1,
        },
        {
            'id': 12,
            'state': 'tag',
            'value': 'generosity',
            'player_id': -1,
        },
        {
            'id': 13,
            'state': 'tag',
            'value': 'humour',
            'player_id': -1,
        },
        {
            'id': 14,
            'state': 'tag',
            'value': 'imagination',
            'player_id': -1,
        },
        {
            'id': 15,
            'state': 'tag',
            'value': 'passion',
            'player_id': -1,
        },
        {
            'id': 16,
            'state': 'tag',
            'value': 'loyalty',
            'player_id': -1,
        },
        {
            'id': 17,
            'state': 'tag',
            'value': 'courage',
            'player_id': -1,
        },
        {
            'id': 18,
            'state': 'tag',
            'value': 'sustainability',
            'player_id': -1,
        },
        {
            'id': 19,
            'state': 'tag',
            'value': 'curiosity',
            'player_id': -1,
        },
        {
            'id': 20,
            'state': 'tag',
            'value': 'openness',
            'player_id': -1,
        },
        {
            'id': 21,
            'state': 'tag',
            'value': 'safety',
            'player_id': -1,
        },
        {
            'id': 22,
            'state': 'tag',
            'value': 'meaningfulness',
            'player_id': -1,
        },
        {
            'id': 23,
            'state': 'tag',
            'value': 'solidarity',
            'player_id': -1,
        },
        {
            'id': 24,
            'state': 'tag',
            'value': 'carefulness',
            'player_id': -1,
        },
        {
            'id': 25,
            'state': 'tag',
            'value': 'pleasure',
            'player_id': -1,
        },
        {
            'id': 26,
            'state': 'tag',
            'value': 'familiarity',
            'player_id': -1,
        },
        {
            'id': 27,
            'state': 'tag',
            'value': 'dignity',
            'player_id': -1,
        },
        {
            'id': 28,
            'state': 'tag',
            'value': 'reliability',
            'player_id': -1,
        },
    ],
}


ubung_3_term_list_i18n = {
    'Deutsch': [
        {
            'id': 0,
            'state': 'tag',
            'value': 'Abhängigkeit',
            'player_id': -1,
        },
        {
            'id': 1,
            'state': 'tag',
            'value': 'Unterordnung',
            'player_id': -1,
        },
        {
            'id': 2,
            'state': 'tag',
            'value': 'Leistungsschwäche',
            'player_id': -1,
        },
        {
            'id': 3,
            'state': 'tag',
            'value': 'Müßiggang',
            'player_id': -1,
        },
        {
            'id': 4,
            'state': 'tag',
            'value': 'Angepasstheit',
            'player_id': -1,
        },
        {
            'id': 5,
            'state': 'tag',
            'value': 'Versagen',
            'player_id': -1,
        },
        {
            'id': 6,
            'state': 'tag',
            'value': 'Starrheit',
            'player_id': -1,
        },
        {
            'id': 7,
            'state': 'tag',
            'value': 'Feindseligkeit',
            'player_id': -1,
        },
        {
            'id': 8,
            'state': 'tag',
            'value': 'Aufgeregtheit',
            'player_id': -1,
        },
        {
            'id': 9,
            'state': 'tag',
            'value': 'Willkür',
            'player_id': -1,
        },
        {
            'id': 10,
            'state': 'tag',
            'value': 'Verkrampftheit',
            'player_id': -1,
        },
        {
            'id': 11,
            'state': 'tag',
            'value': 'Rangordnung',
            'player_id': -1,
        },
        {
            'id': 12,
            'state': 'tag',
            'value': 'Habgier',
            'player_id': -1,
        },
        {
            'id': 13,
            'state': 'tag',
            'value': 'Trübsal',
            'player_id': -1,
        },
        {
            'id': 14,
            'state': 'tag',
            'value': 'Einfallslosigkeit',
            'player_id': -1,
        },
        {
            'id': 15,
            'state': 'tag',
            'value': 'Desinteresse',
            'player_id': -1,
        },
        {
            'id': 16,
            'state': 'tag',
            'value': 'Treulosigkeit',
            'player_id': -1,
        },
        {
            'id': 17,
            'state': 'tag',
            'value': 'Angst',
            'player_id': -1,
        },
        {
            'id': 18,
            'state': 'tag',
            'value': 'Achtlosigkeit',
            'player_id': -1,
        },
        {
            'id': 19,
            'state': 'tag',
            'value': 'Gleichgültigkeit',
            'player_id': -1,
        },
        {
            'id': 20,
            'state': 'tag',
            'value': 'Rechthaberei',
            'player_id': -1,
        },
        {
            'id': 21,
            'state': 'tag',
            'value': 'Risiko',
            'player_id': -1,
        },
        {
            'id': 22,
            'state': 'tag',
            'value': 'Sinnlosigkeit',
            'player_id': -1,
        },
        {
            'id': 23,
            'state': 'tag',
            'value': 'Egoismus',
            'player_id': -1,
        },
        {
            'id': 24,
            'state': 'tag',
            'value': 'Unachtsamkeit',
            'player_id': -1,
        },
        {
            'id': 25,
            'state': 'tag',
            'value': 'Verbot',
            'player_id': -1,
        },
        {
            'id': 26,
            'state': 'tag',
            'value': 'Distanz',
            'player_id': -1,
        },
        {
            'id': 27,
            'state': 'tag',
            'value': 'Ehrlosigkeit',
            'player_id': -1,
        },
        {
            'id': 28,
            'state': 'tag',
            'value': 'Unzuverlässigkeit',
            'player_id': -1,
        },
    ],
    'French': [
        {
            'id': 0,
            'state': 'tag',
            'value': 'dépendance',
            'player_id': -1,
        },
        {
            'id': 1,
            'state': 'tag',
            'value': 'subordination',
            'player_id': -1,
        },
        {
            'id': 2,
            'state': 'tag',
            'value': 'inefficacité',
            'player_id': -1,
        },
        {
            'id': 3,
            'state': 'tag',
            'value': 'oisiveté',
            'player_id': -1,
        },
        {
            'id': 4,
            'state': 'tag',
            'value': 'conformité',
            'player_id': -1,
        },
        {
            'id': 5,
            'state': 'tag',
            'value': 'échec',
            'player_id': -1,
        },
        {
            'id': 6,
            'state': 'tag',
            'value': 'rigidité',
            'player_id': -1,
        },
        {
            'id': 7,
            'state': 'tag',
            'value': 'hostilité',
            'player_id': -1,
        },
        {
            'id': 8,
            'state': 'tag',
            'value': 'décomposition',
            'player_id': -1,
        },
        {
            'id': 9,
            'state': 'tag',
            'value': 'despotisme',
            'player_id': -1,
        },
        {
            'id': 10,
            'state': 'tag',
            'value': 'tension',
            'player_id': -1,
        },
        {
            'id': 11,
            'state': 'tag',
            'value': 'hiérarchie',
            'player_id': -1,
        },
        {
            'id': 12,
            'state': 'tag',
            'value': 'jalousie',
            'player_id': -1,
        },
        {
            'id': 13,
            'state': 'tag',
            'value': 'tristesse',
            'player_id': -1,
        },
        {
            'id': 14,
            'state': 'tag',
            'value': 'ennui',
            'player_id': -1,
        },
        {
            'id': 15,
            'state': 'tag',
            'value': 'léthargie',
            'player_id': -1,
        },
        {
            'id': 16,
            'state': 'tag',
            'value': 'déloyauté',
            'player_id': -1,
        },
        {
            'id': 17,
            'state': 'tag',
            'value': 'peur',
            'player_id': -1,
        },
        {
            'id': 18,
            'state': 'tag',
            'value': 'insouciance',
            'player_id': -1,
        },
        {
            'id': 19,
            'state': 'tag',
            'value': 'indifférence',
            'player_id': -1,
        },
        {
            'id': 20,
            'state': 'tag',
            'value': 'dogmatisme',
            'player_id': -1,
        },
        {
            'id': 21,
            'state': 'tag',
            'value': 'risque',
            'player_id': -1,
        },
        {
            'id': 22,
            'state': 'tag',
            'value': 'absurdité',
            'player_id': -1,
        },
        {
            'id': 23,
            'state': 'tag',
            'value': 'égoïsme',
            'player_id': -1,
        },
        {
            'id': 24,
            'state': 'tag',
            'value': 'négligence',
            'player_id': -1,
        },
        {
            'id': 25,
            'state': 'tag',
            'value': 'interdiction',
            'player_id': -1,
        },
        {
            'id': 26,
            'state': 'tag',
            'value': 'distance ',
            'player_id': -1,
        },
        {
            'id': 27,
            'state': 'tag',
            'value': 'déshonneur',
            'player_id': -1,
        },
        {
            'id': 28,
            'state': 'tag',
            'value': 'incrédibilité',
            'player_id': -1,
        },
    ],
    'Turkish': [
    {'id': 0,  'state': 'tag', 'value': 'bağımlılık',            'player_id': -1},
    {'id': 1,  'state': 'tag', 'value': 'boyuneğme',            'player_id': -1},  # veya itaatkârlık
    {'id': 2,  'state': 'tag', 'value': 'performansdüşüklüğü',  'player_id': -1},
    {'id': 3,  'state': 'tag', 'value': 'aylaklık',              'player_id': -1},  # tembellik
    {'id': 4,  'state': 'tag', 'value': 'uyumculuk',             'player_id': -1},  # aşırı uyum
    {'id': 5,  'state': 'tag', 'value': 'başarısızlık',          'player_id': -1},
    {'id': 6,  'state': 'tag', 'value': 'katılık',               'player_id': -1},
    {'id': 7,  'state': 'tag', 'value': 'düşmanlık',             'player_id': -1},
    {'id': 8,  'state': 'tag', 'value': 'huzursuzluk',           'player_id': -1},  # aşırı heyecan/telaş
    {'id': 9,  'state': 'tag', 'value': 'keyfîlik',              'player_id': -1},
    {'id': 10, 'state': 'tag', 'value': 'gerginlik',             'player_id': -1},  # verkrampftheit
    {'id': 11, 'state': 'tag', 'value': 'hiyerarşi',             'player_id': -1},
    {'id': 12, 'state': 'tag', 'value': 'haset',                 'player_id': -1},  # kıskançlık/haset
    {'id': 13, 'state': 'tag', 'value': 'keder',                 'player_id': -1},
    {'id': 14, 'state': 'tag', 'value': 'yaratıcılıkyoksunluğu','player_id': -1},
    {'id': 15, 'state': 'tag', 'value': 'ilgisizlik',            'player_id': -1},
    {'id': 16, 'state': 'tag', 'value': 'sadakatsizlik',         'player_id': -1},  # vefasızlık
    {'id': 17, 'state': 'tag', 'value': 'korku',                 'player_id': -1},
    {'id': 18, 'state': 'tag', 'value': 'özensizlik',            'player_id': -1},  # achtlosigkeit
    {'id': 19, 'state': 'tag', 'value': 'kayıtsızlık',           'player_id': -1},
    {'id': 20, 'state': 'tag', 'value': 'haklılıktaslama',      'player_id': -1},  # rechthaberei
    {'id': 21, 'state': 'tag', 'value': 'risk',                  'player_id': -1},
    {'id': 22, 'state': 'tag', 'value': 'anlamsızlık',           'player_id': -1},
    {'id': 23, 'state': 'tag', 'value': 'bencillik',             'player_id': -1},
    {'id': 24, 'state': 'tag', 'value': 'dikkatsizlik',          'player_id': -1},
    {'id': 25, 'state': 'tag', 'value': 'yasak',                 'player_id': -1},
    {'id': 26, 'state': 'tag', 'value': 'mesafe',                'player_id': -1},
    {'id': 27, 'state': 'tag', 'value': 'onursuzluk',            'player_id': -1},
    {'id': 28, 'state': 'tag', 'value': 'güvenilmezlik',         'player_id': -1},
    ],
    'Chinese': [
        {
            'id': 0,
            'state': 'tag',
            'value': '依赖性',
            'player_id': -1,
        },
        {
            'id': 1,
            'state': 'tag',
            'value': '从属',
            'player_id': -1,
        },
        {
            'id': 2,
            'state': 'tag',
            'value': '低效率',
            'player_id': -1,
        },
        {
            'id': 3,
            'state': 'tag',
            'value': '懒惰',
            'player_id': -1,
        },
        {
            'id': 4,
            'state': 'tag',
            'value': '符合',
            'player_id': -1,
        },
        {
            'id': 5,
            'state': 'tag',
            'value': '失败',
            'player_id': -1,
        },
        {
            'id': 6,
            'state': 'tag',
            'value': '刚性',
            'player_id': -1,
        },
        {
            'id': 7,
            'state': 'tag',
            'value': '敌意',
            'player_id': -1,
        },
        {
            'id': 8,
            'state': 'tag',
            'value': '混乱',
            'player_id': -1,
        },
        {
            'id': 9,
            'state': 'tag',
            'value': '专制主义',
            'player_id': -1,
        },
        {
            'id': 10,
            'state': 'tag',
            'value': '紧张',
            'player_id': -1,
        },
        {
            'id': 11,
            'state': 'tag',
            'value': '等级制度',
            'player_id': -1,
        },
        {
            'id': 12,
            'state': 'tag',
            'value': '贪欲',
            'player_id': -1,
        },
        {
            'id': 13,
            'state': 'tag',
            'value': '悲伤',
            'player_id': -1,
        },
        {
            'id': 14,
            'state': 'tag',
            'value': '枯燥',
            'player_id': -1,
        },
        {
            'id': 15,
            'state': 'tag',
            'value': '昏昏欲睡',
            'player_id': -1,
        },
        {
            'id': 16,
            'state': 'tag',
            'value': '不忠',
            'player_id': -1,
        },
        {
            'id': 17,
            'state': 'tag',
            'value': '恐惧',
            'player_id': -1,
        },
        {
            'id': 18,
            'state': 'tag',
            'value': '疏忽⼤意',
            'player_id': -1,
        },
        {
            'id': 19,
            'state': 'tag',
            'value': '冷漠',
            'player_id': -1,
        },
        {
            'id': 20,
            'state': 'tag',
            'value': '教条主义',
            'player_id': -1,
        },
        {
            'id': 21,
            'state': 'tag',
            'value': '⻛险',
            'player_id': -1,
        },
        {
            'id': 22,
            'state': 'tag',
            'value': '⽆意义',
            'player_id': -1,
        },
        {
            'id': 23,
            'state': 'tag',
            'value': '私⼼',
            'player_id': -1,
        },
        {
            'id': 24,
            'state': 'tag',
            'value': '粗⼼⼤意',
            'player_id': -1,
        },
        {
            'id': 25,
            'state': 'tag',
            'value': '禁酒令',
            'player_id': -1,
        },
        {
            'id': 26,
            'state': 'tag',
            'value': '距离',
            'player_id': -1,
        },
        {
            'id': 27,
            'state': 'tag',
            'value': '玷污',
            'player_id': -1,
        },
        {
            'id': 28,
            'state': 'tag',
            'value': '不可信',
            'player_id': -1,
        },
    ],
    'English': [
        {
            'id': 0,
            'state': 'tag',
            'value': 'dependency',
            'player_id': -1,
        },
        {
            'id': 1,
            'state': 'tag',
            'value': 'subordination',
            'player_id': -1,
        },
        {
            'id': 2,
            'state': 'tag',
            'value': 'inefficiency',
            'player_id': -1,
        },
        {
            'id': 3,
            'state': 'tag',
            'value': 'idleness',
            'player_id': -1,
        },
        {
            'id': 4,
            'state': 'tag',
            'value': 'conformity',
            'player_id': -1,
        },
        {
            'id': 5,
            'state': 'tag',
            'value': 'failure',
            'player_id': -1,
        },
        {
            'id': 6,
            'state': 'tag',
            'value': 'rigidity',
            'player_id': -1,
        },
        {
            'id': 7,
            'state': 'tag',
            'value': 'hostility',
            'player_id': -1,
        },
        {
            'id': 8,
            'state': 'tag',
            'value': 'discomposure',
            'player_id': -1,
        },
        {
            'id': 9,
            'state': 'tag',
            'value': 'despotism',
            'player_id': -1,
        },
        {
            'id': 10,
            'state': 'tag',
            'value': 'tension',
            'player_id': -1,
        },
        {
            'id': 11,
            'state': 'tag',
            'value': 'hierarchy',
            'player_id': -1,
        },
        {
            'id': 12,
            'state': 'tag',
            'value': 'greediness',
            'player_id': -1,
        },
        {
            'id': 13,
            'state': 'tag',
            'value': 'tribulation',
            'player_id': -1,
        },
        {
            'id': 14,
            'state': 'tag',
            'value': 'dullness',
            'player_id': -1,
        },
        {
            'id': 15,
            'state': 'tag',
            'value': 'lethargy',
            'player_id': -1,
        },
        {
            'id': 16,
            'state': 'tag',
            'value': 'disloyalty',
            'player_id': -1,
        },
        {
            'id': 17,
            'state': 'tag',
            'value': 'fear',
            'player_id': -1,
        },
        {
            'id': 18,
            'state': 'tag',
            'value': 'heedlessness',
            'player_id': -1,
        },
        {
            'id': 19,
            'state': 'tag',
            'value': 'indifference',
            'player_id': -1,
        },
        {
            'id': 20,
            'state': 'tag',
            'value': 'dogmatism',
            'player_id': -1,
        },
        {
            'id': 21,
            'state': 'tag',
            'value': 'risk',
            'player_id': -1,
        },
        {
            'id': 22,
            'state': 'tag',
            'value': 'senselessness',
            'player_id': -1,
        },
        {
            'id': 23,
            'state': 'tag',
            'value': 'selfishness',
            'player_id': -1,
        },
        {
            'id': 24,
            'state': 'tag',
            'value': 'carelessness',
            'player_id': -1,
        },
        {
            'id': 25,
            'state': 'tag',
            'value': 'prohibition',
            'player_id': -1,
        },
        {
            'id': 26,
            'state': 'tag',
            'value': 'distance',
            'player_id': -1,
        },
        {
            'id': 27,
            'state': 'tag',
            'value': 'dishonor',
            'player_id': -1,
        },
        {
            'id': 28,
            'state': 'tag',
            'value': 'untrustworthiness',
            'player_id': -1,
        },
    ],
}



# ubung5 area

def span_choose(user_id, link):

    
    from .models import Game, Player, Ubung1, Ubung3, Ubung5
    game = Game.objects.filter(link=link).first()
    player = Player.objects.filter(id=user_id).first()

    # ubung1_list = [i for i in Ubung1.objects.filter(game=game,state='line-through') if i.player.valid == True]
    ubung1_list = []
    for i in list(Ubung1.objects.filter(game=game,state='line-through')):
        if not i.player:
            continue
        if i.player.valid == True:
            ubung1_list.append(i)

    print('list',ubung1_list)
    ubung1 = None
    for i in ubung1_list:
        if not Ubung5.objects.filter(ubung1=i,player=player).first():
            ubung1 = i
            break
    if not ubung1:
        return None, None
    goal_player = ubung1.player    
    ubung3 = Ubung3.objects.filter(player=goal_player,state='line-through').first()

    return ubung1, ubung3


def span_add(player, target_player, game, score, ubung1_id, ubung3_id):
    from .models import Game, Player, Ubung1, Ubung3, Ubung5
    # game = Game.objects.filter(link=link).first()
    # player = Player.objects.filter(id=user_id).first()
    # target_player = Player.objects.filter(id=target_user_id).first()

    ubung1 = Ubung1.objects.filter(id=ubung1_id).first()
    ubung3 = Ubung3.objects.filter(id=ubung3_id).first()

    ubung5 = Ubung5.objects.create(
        game = game,
        player = player,
        goal = target_player,
        score = score,
        ubung1 = ubung1,
        ubung3 = ubung3,
    )

    return ubung5


# mission 2 ubung 1 area

def m2_span_choose(user_id, link):
    from .models import Game, Player, Ubung1, Ubung3, Ubung5, M2Ubung1
    game = Game.objects.filter(link=link).first()
    player = Player.objects.filter(id=user_id).first()

    ubung5_list = list(Ubung5.objects.filter(game=game, goal=player))
    ubung5 = None
    for i in ubung5_list:
        if not M2Ubung1.objects.filter(ubung1=i.ubung1,player=player).first():
            ubung5 = i 
            break
    return ubung5


    # ubung1_list = [i for i in Ubung1.objects.filter(game=game,state='line-through') if i.player.valid == True]
    # ubung1 = None
    # for i in ubung1_list:
    #     if not M2Ubung1.objects.filter(ubung1=i,player=player).first():
    #         ubung1 = i
    #         break
    # if not ubung1:
    #     return None, None
    # goal_player = ubung1.player    
    # ubung3 = Ubung3.objects.filter(player=goal_player,state='line-through').first()

    return 
    # return ubung1, ubung3


def m2_span_add(player, target_player, game, score, ubung1_id, ubung3_id):
    from .models import Game, Player, Ubung1, Ubung3, M2Ubung1

    ubung1 = Ubung1.objects.filter(id=ubung1_id).first()
    ubung3 = Ubung3.objects.filter(id=ubung3_id).first()

    m2ubung1 = M2Ubung1.objects.create(
        game = game,
        player = player,
        goal = target_player,
        score = score,
        ubung1 = ubung1,
        ubung3 = ubung3,
    )
    
    return m2ubung1


def mean(num_list):
    temp = 0
    if len(num_list) == 0:
        return temp
    else:
        return sum(num_list)/len(num_list)


def add_laststop(user, game):
    from .models import LastStop
    if LastStop.objects.filter(game=game,player=user).first():
        return 
    LastStop.objects.create(
        game = game,
        player = user,
    )


def heatmap_cell(user, game, ubung1):
    from .models import Ubung5
    from .utils import mean
    temp = Ubung5.objects.filter(game=game, goal=user, player=user,ubung1=ubung1).first()
    if temp:
        user_self = Ubung5.objects.filter(game=game, goal=user, player=user,ubung1=ubung1).first().score
    else:
        user_self = 0
    others = [i.score for i in Ubung5.objects.filter(game=game, goal=user, ubung1=ubung1).exclude(player=user)]
    others_avg = round(mean(others), )
    avg = ubung1.ubung5_avg
    ubung5_list = list(Ubung5.objects.filter(game=game,goal=user))
    temp = []
    for i in ubung5_list:
        temp.append(user_self - others_avg)
    return round(sum(temp))

def heatmap_cell_other(user, game, ubung1):
    from .models import Ubung5
    from .utils import mean
    # user_self = Ubung5.objects.filter(game=game, goal=user, player=user,ubung1=ubung1).first().score
    others = [i.score for i in Ubung5.objects.filter(game=game, goal=user, ubung1=ubung1).exclude(player=user)]
    others_avg = round(mean(others), )
    avg = ubung1.ubung5_avg
    ubung5_list = list(Ubung5.objects.filter(game=game,goal=user))
    temp = []
    for i in ubung5_list:
        temp.append(others_avg)
    return round(sum(temp))

def heatmap_color(user, game, ubung1):
    from .models import Ubung5
    from .utils import mean
    low_bond = ubung1.ubung5_avg - 16
    high_bond = ubung1.ubung5_avg + 16

    temp = Ubung5.objects.filter(game=game, goal=user, player=user,ubung1=ubung1).first()
    if temp:
        user_self = Ubung5.objects.filter(game=game, goal=user, player=user,ubung1=ubung1).first().score
    else:
        user_self = 0
    others = [i.score for i in Ubung5.objects.filter(game=game, goal=user, ubung1=ubung1).exclude(player=user)]
    others_avg = mean(others)

    if (user_self < low_bond) or (user_self > high_bond):
        if (others_avg < low_bond) or (others_avg > high_bond):
            return 'black'
        else:
            return 'red'
    else:
        if (others_avg < low_bond) or (others_avg > high_bond):
            return 'yellow'
        else:
            return 'None'
