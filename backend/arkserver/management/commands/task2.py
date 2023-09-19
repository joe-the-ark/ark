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

        for name in self.get_games(options['games']):
            game = Game.objects.filter(name=name).first()
            if not game: continue

            n, u1u3 = self.handle_game(game)
            for power in u1u3:
                item = u1u3[power]
                if power not in result:
                    result[power] = { 'count': 0, 'opposites': {} }

                result[power]['count'] += item['count']
                for drainer in item['opposites']:
                    if drainer not in result[power]['opposites']:
                        result[power]['opposites'][drainer] = 0
                    result[power]['opposites'][drainer] += item['opposites'][drainer]

        for power in sorted(result.keys(), key=lambda x:result[x]['count'], reverse=True):
            drainers = result[power]['opposites']
            top_5 = sorted(drainers.keys(), key=lambda x:drainers[x], reverse=True)[:5]
            print(power, result[power]['count'])
            for drainer in top_5:
                print(f'\t{drainer}: {drainers[drainer]}')

    """
    #2 Display the list of safety anchors, with its opposites, ranked by how often they’ve been chosen
    """
    def handle_game(self, game):
        n = get_n(game)
        result = get_u1_u3(game)
        return n, result
