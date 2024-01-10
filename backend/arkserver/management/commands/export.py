from django.core.management import BaseCommand
from arkserver.models import *
from .utils import *
from itertools import combinations
import math

class Command(BaseCommand):

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

            csv_file = self.handle_game(game)
            print(csv_file)

    def handle_game(self, game):
        votes, n = get_u5(game)

        headers = []
        players = {}
        indices = {}
        cnt = 0
        for player in votes:
            indices[player] = cnt
            headers.append(player)
            cnt += 1
            players[player] = 'Player'+cnt

        txt = ',,' + ','.join(headers) + '\n'

        for player in votes:
            pvotes = votes[player]
            txt += f'{players[player]},'
            for power in pvotes:
                txt += f'{power},'
                cell = pvotes[power]

                scores = [0]*n
                for goal in cell:
                    index = indices[goal]
                    score = cell[goal]
                    scores[index] = score

                txt += ','.join([str(_) for _ in scores])

        return txt
