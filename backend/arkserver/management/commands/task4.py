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

        r3 = lambda x: round(x)
        p2 = lambda x: f"{round(x*100)}%"

        for name in self.get_games(options['games']):
            game = Game.objects.filter(name=name).first()
            if not game: continue

            result, n, votes, given, avg, safezone = self.handle_game(game)
            def get_color(player, power):
                cell = result[player][power]
                baseline = round(safezone[power])
                selfsafe = (baseline-16) <= cell['self'] <= (baseline+16)
                othersafe = (baseline-16) <= cell['other'] <= (baseline+16)
                if selfsafe and othersafe:
                    return 'green'
                if selfsafe and not othersafe:
                    return 'yellow'
                if not selfsafe and othersafe:
                    return 'red'
                if not selfsafe and not othersafe:
                    return 'black'

            def is_safe(power, v):
                baseline = safezone[power]
                return (baseline-16) <= v <= (baseline+16)

            print (f'Game: {game.name}')
            print (f'Player\tAvg\tOther\tSum\tGreen\tYellow\tRed\tBlack\tSafe1\tUnsafe1\tSafe2\tUnsafe2')
            for player in result:
                avg_other = sum([result[player][power]['other'] for power in result[player]]) / n
                sum_tension = sum([
                    result[player][power]['diff']
                for power in result[player]])

                colors = { 'green': 0, 'yellow': 0, 'red': 0, 'black': 0 }
                for power in result[player]:
                    color = get_color(player, power)
                    colors[color] += 1/n

                safe_got = 0
                unsafe_got = 0
                for power in votes[player]:
                    for p in votes[player][power]:
                        v = votes[player][power][p]
                        if is_safe(power, v):
                            safe_got += 1/n**2
                        else:
                            unsafe_got += 1/n**2

                safe_given = 0
                unsafe_given = 0
                for power in given[player]:
                    for p in given[player][power]:
                        v = given[player][power][p]
                        if is_safe(power, v):
                            safe_given += 1/n**2
                        else:
                            unsafe_given += 1/n**2

                print(f'{player[:5]}\t{r3(avg[player])}\t{r3(avg_other)}\t{r3(sum_tension)}\t{p2(colors["green"])}\t{p2(colors["yellow"])}\t{p2(colors["red"])}\t{p2(colors["black"])}\t{p2(safe_got)}\t{p2(unsafe_got)}\t{p2(safe_given)}\t{p2(unsafe_given)}')

    def handle_game(self, game):
        votes, n = get_u5(game)
        
        result = {}
        given = {}
        safezone = {}
        avg = {}

        for player in votes:
            result[player] = {}
            given[player] = {}

        for player in votes:
            pvotes = votes[player]
            total = 0
            for power in pvotes:
                s = 0
                o = 0
                cell = pvotes[power]
                for p in cell:
                    if power not in given[p]:
                        given[p][power] = {}
                    given[p][power][player] = cell[p]
                    if p == player:
                        s = cell[p]
                    else:
                        o += cell[p]
                r = result[player][power] = {}
                total += (s+o)

                r['self'] = s
                r['other'] = o / (n-1)
                r['diff'] = s - r['other']

            avg[player] = total / n**2

        for player in result:
            for power in result[player]:
                if power not in safezone:
                    safezone[power] = 0
                safezone[power] += result[player][power]['other'] / n

        return result, n, votes, given, avg, safezone
