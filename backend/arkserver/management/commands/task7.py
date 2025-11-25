from django.core.management import BaseCommand
from arkserver.models import *
from .utils import *

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("games", nargs="*", type=str)

    def get_games(self, games):
        if games: return games
        return [_.name for _ in Game.objects.all() if not 'test' in _.name.lower() and get_n(_) > 2]

    def handle(self, **options):
        for name in self.get_games(options['games']):
            game = Game.objects.filter(name=name).first()
            if not game: continue

            self.handle_game(game)

    def handle_game(self, game):

        print('='*20)
        print(f'Game: {game.name}')
        players = game.members.all()
        nplayers = WaitingRoomMember.objects.filter(game=game,state=1)
        n = nplayers.count()

        print(f'Player count: {n}')

        r0, r1, r2, r3, r4, r5 = 0, 0, 0, 0, 0, 0
        w0, w1, w2, w3, w4, w5 = 4, 1, 3, 5, 0, 2
        print("\ttopics\texcl\tinvis\tseen\tblame\thelp\tTotal")
        qs = Ubung4.objects.filter(game=game)
        for p in nplayers:
            player = p.player
            u4 = qs.filter(player=player).first()
            _r0 = u4.row0.count() if u4 else 0
            _r1 = u4.row1.count() if u4 else 0
            _r2 = u4.row2.count() if u4 else 0
            _r3 = u4.row3.count() if u4 else 0
            _r4 = u4.row4.count() if u4 else 0
            _r5 = u4.row5.count() if u4 else 0
            r0 += _r0
            r1 += _r1
            r2 += _r2
            r3 += _r3
            r4 += _r4
            r5 += _r5
            _u4 = _r0*w0+_r1*w1+_r2*w2+_r3*w3+_r4*w4+_r5*w5
            _u4 = _u4*20/n
            print(f'{player.name[:7]}\t{_r0}\t{_r1}\t{_r2}\t{_r3}\t{_r4}\t{_r5}\t{round(_u4)}')

        u4_score = r0*w0+r1*w1+r2*w2+r3*w3+r4*w4+r5*w5
        u4_score = u4_score * 20 / n**2
        print(f'Total\t{r0}\t{r1}\t{r2}\t{r3}\t{r4}\t{r5}\t{round(u4_score)}')
