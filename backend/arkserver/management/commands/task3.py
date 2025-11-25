from django.core.management import BaseCommand
from arkserver.models import *
from .utils import *

class Command(BaseCommand):
    help = "Stress > how much tension the votes of a player creates (projection) – the values from"

    def add_arguments(self, parser):
        parser.add_argument("games", nargs="*", type=str)

    def get_games(self, games):
        if games: return games
        return [_.name for _ in Game.objects.all() if not 'test' in _.name.lower() and get_n(_) > 1]

    def handle(self, **options):
        result = {}
        for name in self.get_games(options['games']):
            game = Game.objects.filter(name=name).first()
            if not game: continue

            n, u5b = self.handle_game(game)
            for player in u5b:
                if u5b[player] == 0:
                    continue

                if player not in result:
                    result[player] = { 'total': 0, 'count': 0, 'games': {} }
                result[player]['total'] += u5b[player]
                result[player]['count'] += 1
                result[player]['games'][game.name] = u5b[player]

        for player in result:
            result[player]['avg'] = result[player]['total'] / result[player]['count']

        print('Player', '\t', 'Avg', '\t', 'Games', '\t', 'Details(top 5)')
        for player in sorted(result.keys(), key=lambda x: result[x]['avg'], reverse=True):
            avg = round(result[player]['avg'])
            if not avg: continue

            top5 = sorted(result[player]['games'].keys(), key=lambda x: result[player]['games'][x], reverse=True)[:5]

            print(player[:6], '\t', avg, '\t', result[player]['count'], '\t', '\t'.join([f'{_}:{round(result[player]["games"][_])}' for _ in top5]))
    
    """
    List: tension in the game (U5 AVG), display the average value of the votes a player gives to others -> for all players across a
    game -> for all selected games.
    """
    def handle_game(self, game):
        n = get_n(game)
        u5b = get_u5b(game)
        return n, u5b
