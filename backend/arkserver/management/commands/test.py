from django.core.management import BaseCommand
from arkserver.models import *

class Command(BaseCommand):
    def handle(self, **kwargs):
        for game in Game.objects.filter():
            if 'test' in game.name.lower() or game.members.count() <= 2:
                continue

            if game.name != 'TeamC': continue

            self.handle_game(game)

    def handle_game(self, game):
        #name = 'Logistikreise'
        #game = Game.objects.filter(name=name).first()

        print('='*20)
        print(f'Game: {game.name}')
        players = game.members.all()
        nplayers = WaitingRoomMember.objects.filter(game=game,state=1)
        n = nplayers.count()

        print(f'Player count: {n}')

        u2_score = 0
        for player in players:
            u2 = Ubung2.objects.filter(game=game, player=player).first()
            if not u2: continue

            value = u2.value
            print(f'U2: {player.name} - {value}')
            u2_score += value

        u2_score /= n
        print(f'U2 AVG: {u2_score}')

        r0, r1, r2, r3, r4, r5 = 0, 0, 0, 0, 0, 0
        w0, w1, w2, w3, w4, w5 = 4, 1, 3, 5, 0, 2
        print("\ttopics\texcl\tinvis\tseen\tblame\thelp\tTotal")
        for vote in Ubung4.objects.filter(game=game):
            _r0 = vote.row0.count()
            _r1 = vote.row1.count()
            _r2 = vote.row2.count()
            _r3 = vote.row3.count()
            _r4 = vote.row4.count()
            _r5 = vote.row5.count()
            r0 += _r0
            r1 += _r1
            r2 += _r2
            r3 += _r3
            r4 += _r4
            r5 += _r5
            _u4 = _r0*w0+_r1*w1+_r2*w2+_r3*w3+_r4*w4+_r5*w5
            _u4 = _u4*20/n
            print(f'{vote.player.name[:7]}\t{vote.row0.count()}\t{vote.row1.count()}\t{vote.row2.count()}\t{vote.row3.count()}\t{vote.row4.count()}\t{vote.row5.count()}\t{_u4}')

        u4_score = r0*w0+r1*w1+r2*w2+r3*w3+r4*w4+r5*w5
        u4_score = u4_score * 20 / n**2
        print(f'Total\t{r0}\t{r1}\t{r2}\t{r3}\t{r4}\t{r5}\t{u4_score}')

        u1_items = Ubung1.objects.filter(game=game)
        for item in u1_items:
            print(f'{item.player.name}: {item.power}')


        u3_items = Ubung3.objects.filter(game=game)
        for item in u3_items:
            print(f'{item.player.name}: {item.drainer}')

