from django.core.management import BaseCommand
from arkserver.models import *
from .utils import *
from datetime import datetime

class Command(BaseCommand):
    help = "Task1: Perceived team performance across the team"

    def add_arguments(self, parser):
        parser.add_argument("games", nargs="*", type=str)
        parser.add_argument("-start", type=str)
        parser.add_argument("-end", type=str)

    def get_games(self, games):
        if games: return games
        return [_.name for _ in Game.objects.all() if not 'test' in _.name.lower() and get_n(_) > 2]

    def handle(self, **options):
        print ("Name\tPlayers\tU2 AVG\tU4 AVG\tU5 AVG\tU2-U4\tU2-(100-U5)\tDate")
        start_time = options['start']
        end_time = options['end']

        total = [0, 0, 0, 0, 0, 0]
        count = 0
        for name in self.get_games(options['games']):
            game = Game.objects.filter(name=name).first()
            if not game: continue

            if start_time and game.create_time.replace(tzinfo=None) < datetime.strptime(start_time, '%Y.%m'):
                continue

            if end_time and game.create_time.replace(tzinfo=None) > datetime.strptime(end_time, '%Y.%m'):
                continue

            n, u2, u4, u5 = self.handle_game(game)
            if u4 == 0 or u5 == 0:
                continue

            total[0] += n
            total[1] += u2
            total[2] += u4
            total[3] += u5

            count += 1
            print(f'{game.name[:7]}\t{n}\t{u2}\t{u4}\t{u5}\t{u2-u4}\t{u2-(100-u5)}\t{game.create_time.strftime("%Y.%m.%d")}')

        print('='*20)
        print(f'Total\t{r1(total[0])}\t{r1(total[1])}\t{r1(total[2])}\t{r1(total[3])}\t{r1(total[1]-total[2])}\t{r1(total[1]-(100*count-total[3]))}')
        f = lambda x: round(x/count)
        print(f'Avg\t{f(total[0])}\t{f(total[1])}\t{f(total[2])}\t{f(total[3])}\t{f(total[1]-total[2])}\t{f(total[1]-(100*count-total[3]))}')
    """
    #1 Display a list of selected games that connects U2 AVG, U4 AVG and U5 AVG based on the two hypothesis
    that connect the 3 values (mock-up of a possible visualisation in the appendix); #4 plot the data point on a graph.
    """
    def handle_game(self, game):
        n = get_n(game)
        u2_avg = get_u2_avg(game)
        u4_avg = get_u4_avg(game)
        u5_avg = get_u5_avg(game)
        return n, round(u2_avg), round(u4_avg), round(u5_avg)
