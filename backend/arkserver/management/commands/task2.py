from django.core.management import BaseCommand
from arkserver.models import *
from .utils import *

class Command(BaseCommand):
    help = "Task2: Safety anchors"

    def add_arguments(self, parser):
        parser.add_argument("games", nargs="*", type=str)

    def get_games(self, games):
        if games: return games
        return [_.name for _ in Game.objects.all() if not 'test' in _.name.lower() and get_n(_) > 2]

    def handle(self, **options):
        result = {}

        def get_names(lookup, id):
            names = []
            for lang in lookup:
                items = lookup[lang]
                for item in items:
                    if item['id'] == id:
                        names.append(item['value'])
            if not names:
                names.append(id)
            return ','.join(names)

        for name in self.get_games(options['games']):
            game = Game.objects.filter(name=name).first()
            if not game: continue

            n, u1u3 = self.handle_game(game)
            for power in u1u3:
                item = u1u3[power]
                if power not in result:
                    result[power] = { 'count': 0, 'opposites': {}, 'u5_sum': 0, 'u5_cnt': 0, 'players':[] }

                result[power]['count'] += item['count']
                result[power]['players'] += item['players']
                result[power]['u5_sum'] += item['u5_sum']
                result[power]['u5_cnt'] += item['u5_cnt']
                for drainer in item['opposites']:
                    if drainer not in result[power]['opposites']:
                        result[power]['opposites'][drainer] = { 'count': 0, 'u5_sum': 0, 'u5_cnt': 0, 'players': [] }
                    result[power]['opposites'][drainer]['count'] += item['opposites'][drainer]['count']
                    result[power]['opposites'][drainer]['players'] += item['opposites'][drainer]['players']
                    result[power]['opposites'][drainer]['u5_sum'] += item['opposites'][drainer]['u5_sum']
                    result[power]['opposites'][drainer]['u5_cnt'] += item['opposites'][drainer]['u5_cnt']

        for power in sorted(result.keys(), key=lambda x:result[x]['count'], reverse=True):
            drainers = result[power]['opposites']
            top_5 = sorted(drainers.keys(), key=lambda x:drainers[x]['count'], reverse=True)[:5]
            print(f"[{get_names(ubung_1_term_list_i18n, power)}]: {result[power]['count']} ({','.join(result[power]['players'])}) <{round(result[power]['u5_sum']/result[power]['u5_cnt'])}>")
            for drainer in top_5:
                print(f"\t[{get_names(ubung_3_term_list_i18n, drainer)}]: {drainers[drainer]['count']} ({','.join(drainers[drainer]['players'])}) <{round(drainers[drainer]['u5_sum']/drainers[drainer]['u5_cnt'])}>")
            print()
    """
    #2 Display the list of safety anchors, with its opposites, ranked by how often they’ve been chosen
    """
    def handle_game(self, game):
        n = get_n(game)
        result = get_u1_u3(game)
        return n, result
