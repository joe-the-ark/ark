from django.db import models
from .utils import ubung_1_term_list_i18n, ubung_3_term_list_i18n

# Create your models here.

class Player(models.Model):
    name = models.CharField(max_length=100, verbose_name='player_name')
    # avatar = models.ImageField(upload_to='avatar', default='', blank=True, null=True)
    avatar = models.CharField(max_length=100, default='', blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)

    # nickname = models.CharField(max_length=100, verbose_name='nickname', default='')
    # openid = models.CharField(max_length=100, verbose_name='openid', default='')
    # game_secret = models.CharField(max_length=200, verbose_name='game_password', null=True, blank=True)
    # game_name = models.CharField(max_length=200, verbose_name='game_name')
    # inviter_name = models.CharField(max_length=200, verbose_name='creater')

    @property
    def valid(self):
        # the qualification that the user have already pass the waiting room
        player_ = WaitingRoomMember.objects.filter(player=self).first()
        if player_.state == 1:
            return True
        else:
            return False

    @property
    def player_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'avatar': self.avatar,
        }

    @property
    def ubung5_sum(self):
        from .models import Ubung5
        temp = [i.score for i in list(Ubung5.objects.filter(goal=self))]
        return sum(temp)

    class Meta(object):
            verbose_name = verbose_name_plural = 'players'

    def __str__(self):
        return self.name

class Game(models.Model):
    name = models.CharField(max_length=200, verbose_name='game_name')
    link = models.CharField(max_length=200, verbose_name='game_link')
    creator = models.ForeignKey(Player,related_name='creator',on_delete=models.CASCADE,verbose_name='creator')
    members = models.ManyToManyField(Player, blank=True, null=True)
    status = models.IntegerField(
        default=0,
        # "start" means the game is start and the waiting room is open for another players
        # "running" means the game is starting
        # "end" means the game is closed
        choices=((0, 'start'), (1, 'running'), (2, 'end')),
        verbose_name='game_status'
    )
    create_time = models.DateTimeField(auto_now_add=True)

    @property
    def valid_players(self):
        temp = self.members.all()
        result = []
        for i in list(temp):
            if i.valid:
                result.append(i)
        return result
        
    @property
    def ubung5_player_order(self):
        from .models import Player
        player_list = []
        # print(self.members.all())
        for i in self.members.all():
            if i.valid:
                player_list.append(i)

        player_list.sort(key=lambda x: x.ubung5_sum, reverse=True)
        
        return player_list
    
    @property
    def ubung5_scale_order(self):
        from .models import Ubung5
        ubung5 = Ubung5.objects.filter(game=self)
        temp = []
        for i in ubung5:
            temp.append(i.ubung1)
        ubung1_list = list(set(temp))
        ubung1_list.sort(key=lambda x: x.ubung5_sum, reverse=True)
        return ubung1_list

    @property
    def ubung4_target(self):
        from .models import Ubung4
        ubung4_list = list(Ubung4.objects.filter(game=self))
        row0 = []
        row1 = []
        row2 = []
        row3 = []
        row4 = []
        row5 = []
        for i in ubung4_list:
            for u in i.row0.all():
                row0.append(u.player_json)
            for u in i.row1.all():
                row1.append(u.player_json)
            for u in i.row2.all():
                row2.append(u.player_json)
            for u in i.row3.all():
                row3.append(u.player_json)
            for u in i.row4.all():
                row4.append(u.player_json)
            for u in i.row5.all():
                row5.append(u.player_json)
        result = {
            'row0': row0,
            'row1': row1,
            'row2': row2,
            'row3': row3,
            'row4': row4,
            'row5': row5,
        }

        return result

    class Meta(object):
            verbose_name = verbose_name_plural = 'games'

    def __str__(self):
        return 'name:' + self.name + '，' + 'creator:'


class WaitingRoomMember(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='game')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='player')
    state = models.IntegerField(
        default = 0,
        choices = ((0, 'not ready'), (1, 'ready'), (2, 'end')),
        verbose_name = 'player waiting room state'
    )
    create_time = models.DateTimeField(auto_now_add=True)

    @property
    def json(self):
        return {
            'game': self.game.link,
            'name': self.palyer.name,
            'avatar': self.palyer.avatar,
            'state': self.state,
        }

    class Meta(object):
        verbose_name = verbose_name_plural = 'room member'

    def __str__(self):
        return self.game.name


class Ubung1(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='game')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='player', blank=True, null=True,)
    power = models.CharField(max_length=100, default='')
    # 2 state: 'tag', 'line-through'
    state = models.CharField(max_length=100, default='')
    create_time = models.DateTimeField(auto_now_add=True)

    @property
    def power_i18n(self):
        result = {}
        result['en'] = self.power

        item_id = -1
        for i in ubung_1_term_list_i18n['English']:
            if i['value'] == self.power:
                item_id = i['id']
                break
        if item_id == -1:
            result['de'] = self.power
            result['fr'] = self.power
            result['zh-hans'] = self.power
            return result
        
        for i in ubung_1_term_list_i18n['Deutsch']:
            if i['id'] == item_id:
                result['de'] = i['value']
                break
        for i in ubung_1_term_list_i18n['French']:
            if i['id'] == item_id:
                result['fr'] = i['value']
                break
        for i in ubung_1_term_list_i18n['Chinese']:
            if i['id'] == item_id:
                result['zh-hans'] = i['value']
                break
    
        return result

    @property
    def connect_ubung3(self):
        from .models import Ubung5
        ubung3 = Ubung5.objects.filter(game=self.game, ubung1=self).first().ubung3
        if ubung3:
            return ubung3
        else:
            return None

    @property
    def ubung5_sum(self):
        from .models import Ubung5
        temp = [i.score for i in list(Ubung5.objects.filter(ubung1=self,game=self.game))]
        return sum(temp)

    @property
    def ubung5_avg(self):
        from .models import Ubung5
        temp = [i.score for i in list(Ubung5.objects.filter(ubung1=self))]
        from .utils import mean
        return mean(temp)

    @property
    def json(self):
        return {
            'game': self.game.link,
            'player': self.player.name,
            'power': self.power,
            'state': self.state,
        }
    
    @property
    def api_json(self):
        if self.player:    
            return {
                'state': self.state,
                'value': self.power,
                'player_id': self.player.id,
            }
        else:
            return {
                'state': self.state,
                'value': self.power,
                'player_id': -1,
            }

    class Meta(object):
        verbose_name = verbose_name_plural = 'Ubung-1'
    
    def __str__(self):
        # return f'{self.game.name} {self.player.name} {self.power}'
        if self.player:
            return f'{self.game.name} {self.player.name} {self.power}'
        else:
            return f'{self.game.name} None {self.power}'



class Ubung2(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='game')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='player')
    value = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)

    @property
    def json(self):
        return {
            'game': self.game.link,
            'player': self.player.name,
            'value': self.value,
        }  

    class Meta(object):
        verbose_name = verbose_name_plural = 'Ubung-2'
    def __str__(self):
        return f'{self.game.name} {self.player.name} {self.value}'


class Ubung3(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='game')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='player', blank=True, null=True,)
    drainer = models.CharField(max_length=100, default='')
    # 2 state: 'tag', 'line-through'
    state = models.CharField(max_length=100, default='')
    create_time = models.DateTimeField(auto_now_add=True)

    @property
    def drainer_i18n(self):
        result = {}
        result['en'] = self.drainer

        item_id = -1
        for i in ubung_3_term_list_i18n['English']:
            if i['value'] == self.drainer:
                item_id = i['id']
                break
        if item_id == -1:
            result['de'] = self.drainer
            result['fr'] = self.drainer
            result['zh-hans'] = self.drainer
            return result
        
        for i in ubung_3_term_list_i18n['Deutsch']:
            if i['id'] == item_id:
                result['de'] = i['value']
                break
        for i in ubung_3_term_list_i18n['French']:
            if i['id'] == item_id:
                result['fr'] = i['value']
                break
        for i in ubung_3_term_list_i18n['Chinese']:
            if i['id'] == item_id:
                result['zh-hans'] = i['value']
                break

        return result

    @property
    def connect_ubung1(self):
        from .models import Ubung1
        ubung1 = Ubung1.objects.filter(player=self.player).first()
        if ubung1:
            return ubung1
        else:
            return None

    @property
    def json(self):
        return {
            'game': self.game.link,
            'player': self.player.name,
            'drainer': self.drainer,
        }

    @property
    def api_json(self):
        if self.player:    
            return {
                'state': self.state,
                'value': self.drainer,
                'player_id': self.player.id,
            }
        else:
            return {
                'state': self.state,
                'value': self.drainer,
                'player_id': -1,
            }

    class Meta(object):
        verbose_name = verbose_name_plural = 'Ubung-3'
    
    def __str__(self):
        if self.player:
            return f'{self.game.name} {self.player.name} {self.drainer}'
        else:
            return f'{self.game.name} None {self.drainer}'

class Ubung4(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='game')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='author')
    
    # for 'Probleme und schwierige Themen kann ich bei dir ansprechen.'
    row0 = models.ManyToManyField(Player, blank=True, null=True, related_name='row0')

    # for 'Du schliesst manchmal Menschen aus dem Team aus, weil sie anders sind.'
    row1 = models.ManyToManyField(Player, blank=True, null=True, related_name='row1')

    # for 'Du arbeitest manchmal im Team auch gegen mich.'
    row2 = models.ManyToManyField(Player, blank=True, null=True, related_name='row2')

    # for 'Meine Talente werden von dir gesehen, geschätzt und ausgeschöpft.'
    row3 = models.ManyToManyField(Player, blank=True, null=True, related_name='row3')
    
    # for 'Wenn im Team Fehler passieren, verwendest du das gegen die Betroffenen.'
    row4 = models.ManyToManyField(Player, blank=True, null=True, related_name='row4')

    # for 'Es fällt mir schwer, dich um Hilfe zu bitten.'
    row5 = models.ManyToManyField(Player, blank=True, null=True, related_name='row5')

    @property
    def row0_json(self):
        result = []
        for i in self.row0.all():
            result.append(i.player_json)
        return result

    @property
    def row1_json(self):
        result = []
        for i in self.row1.all():
            result.append(i.player_json)
        return result

    @property
    def row2_json(self):
        result = []
        for i in self.row2.all():
            result.append(i.player_json)
        return result

    @property
    def row3_json(self):
        result = []
        for i in self.row3.all():
            result.append(i.player_json)
        return result

    @property
    def row4_json(self):
        result = []
        for i in self.row4.all():
            result.append(i.player_json)
        return result


    @property
    def row5_json(self):
        result = []
        for i in self.row5.all():
            result.append(i.player_json)
        return result
    

    class Meta(object):
        verbose_name = verbose_name_plural = 'Ubung-4'
    def __str__(self):
        return f'{self.game}---{self.player}'


class Ubung5(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='game')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='author')
    goal = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='goal',related_name='goal')
    score = models.IntegerField(default=0)

    ubung1 = models.ForeignKey(Ubung1, related_name='ubung_1', on_delete=models.CASCADE, blank=True, null=True)
    ubung3 = models.ForeignKey(Ubung3, related_name='ubung_3', on_delete=models.CASCADE, blank=True, null=True)

    @property
    def span_1(self):
        return {
            'id': self.player.id,
            'name': self.player.name,
            'value': self.ubung1.power + ' '+ self.ubung3.drainer,
            'ubung1_power_i18n': self.ubung1.power_i18n,
            'ubung3_drainer_i18n': self.ubung3.drainer_i18n,
            'avatar': self.player.avatar,
            'statusSide': self.score,
            'target_user': self.goal.name,
            'target_user_avatar': self.goal.avatar,
        }

    class Meta(object):
        verbose_name = verbose_name_plural = 'Ubung-5'
    def __str__(self):
        return f'{self.game} -- {self.player} -- {self.goal} -- {self.score}'
    

class M2Ubung1(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='game')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='author')
    goal = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='goal',related_name='m2_goal')
    score = models.IntegerField(default=0)

    ubung1 = models.ForeignKey(Ubung1, related_name='ubung_1_for_m2', on_delete=models.CASCADE, blank=True, null=True)
    ubung3 = models.ForeignKey(Ubung3, related_name='ubung_3_for_m2', on_delete=models.CASCADE, blank=True, null=True)

    class Meta(object):
        verbose_name = verbose_name_plural = 'M2Ubung1'
    def __str__(self):
        return f'{self.game} -- {self.player} -- {self.goal} -- {self.score}'

class M2Ubung2(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='game')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='author')
    goal = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='goal',related_name='m2_goal2')

    row1 = models.TextField()
    row2 = models.TextField()
    row3 = models.TextField()
    
    class Meta(object):
        verbose_name = verbose_name_plural = 'M2Ubung2'
    def __str__(self):
        return f'{self.game} -- {self.player} -- {self.goal}'

class LastStop(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='game')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='author')

    class Meta(object):
        verbose_name = verbose_name_plural = 'LastStop'
    def __str__(self):
        return f'{self.game}--{self.player}'

class Waitingroom2(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='game')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='author')

    create_time = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        verbose_name = verbose_name_plural = 'Waitingroom2'

    def __str__(self):
        return f"{self.game} --- {self.player}"


class Waitingroom2Start(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='game')
    # 0 is not open, 1 is open
    status = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    
    class Meta(object):
        verbose_name = verbose_name_plural = 'Waitingroom2Start'
    def __str__(self):
        return f"{self.game} -- {self.status}"

class Waitingroom3(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='game')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='author')

    create_time = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        verbose_name = verbose_name_plural = 'Waitingroom2'

    def __str__(self):
        return f"{self.game} --- {self.player}"


class Waitingroom3Start(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='game')
    # 0 is not open, 1 is open
    status = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        verbose_name = verbose_name_plural = 'Waitingroom2Start'
    def __str__(self):
        return f"{self.game} -- {self.status}"



# class Character(models.Model):
#     name = models.CharField(max_length=100, verbose_name='scale')

#     class Meta(object):
#             verbose_name = verbose_name_plural = 'scales'

#     def __str__(self):
#         return self.name

# class CharacterChoose(models.Model):
#     character_one = models.ForeignKey(Character, on_delete=models.CASCADE, verbose_name='scale_one', related_name='character_one')
#     character_two = models.ForeignKey(Character, on_delete=models.CASCADE, verbose_name='scale_two', related_name='character_two')
#     player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='chooser')
#     game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='game')
#     status = models.IntegerField(
#         default=0,
#         choices=((0, 'nomal'), (1, 'showed')),
#         verbose_name='status'
#     )

#     class Meta(object):
#             verbose_name = verbose_name_plural = 'tension_scale'

#     def __str__(self):
#         return self.character_one.name +','+self.character_two.name

# class PlayerScore(models.Model):
#     character_choose = models.ForeignKey('CharacterChoose', on_delete=models.CASCADE)
#     score = models.CharField(max_length=100, verbose_name='score')
#     scorer = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='voting_person', related_name='scorer_score')
#     player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='voted_person', related_name='player_score')
#     game = models.ForeignKey('Game', on_delete=models.CASCADE, verbose_name='game')

#     class Meta(object):
#             verbose_name = verbose_name_plural = 'voting'

#     def __str__(self):
#         return self.player.name + ':'+ self.score


# class GameProcess(models.Model):

#     class Meta(object):
#         verbose_name = verbose_name_plural = 'progress'

#     game = models.ForeignKey('Game', on_delete=models.CASCADE, verbose_name='game')
#     player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='player')
#     process = models.CharField(max_length=100, verbose_name='progress')

#     def __str__(self):
#         return self.game.game_name+'__'+self.player.name+'__'+self.process


# class FirstScore(models.Model):
#     class Meta(object):
#         verbose_name = verbose_name_plural = 'first score'

#     first_score = models.CharField(max_length=20, verbose_name='first score')
#     game = game = models.ForeignKey('Game', on_delete=models.CASCADE, verbose_name='game')
#     player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='player')


#     def __str__(self):
#         return self.player.name + '__firstScore:'+self.first_score


# class Feedback(models.Model):
#     love = models.CharField(max_length=500, verbose_name='love')
#     add = models.CharField(max_length=500, verbose_name='add')
#     ask = models.CharField(max_length=500, verbose_name='ask')
    
#     player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='player', related_name='player')
#     teammate = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='teammate', related_name='teammate')
#     game = models.ForeignKey('Game', on_delete=models.CASCADE, verbose_name='game')

#     def __str__(self):
#         return self.game.game_name+'__'+self.player.name


# class Result(models.Model):
#     name = models.CharField(max_length=500,default='')
#     player = models.CharField(max_length=500,default='')
#     game_secret = models.CharField(max_length=500, default='')
#     inviter = models.CharField(max_length=100, default='')
#     img = models.FileField(upload_to='result/')



