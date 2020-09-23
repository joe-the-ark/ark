from django.db import models

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
    def player_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'avatar': self.avatar,
        }

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
        # "running" means the game is running, waiting room is not open
        # "end" means the game is closed
        choices=((0, 'start'), (1, 'running'), (2, 'end')),
        verbose_name='game_status'
    )
    create_time = models.DateTimeField(auto_now_add=True)
    
    # game_secret = models.CharField(max_length=200, verbose_name='game_password', null=True, blank=True)
    # inviter = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='creater', related_name='inviter_game')
    # status = models.IntegerField(
    #     default=0,
    #     choices=((0, 'start'), (1, 'running'), (2, 'end')),
    #     verbose_name='game_status'
    # )

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
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='player')
    power = models.CharField(max_length=100, default='')
    # 2 state: 'tag', 'line-through'
    state = models.CharField(max_length=100, default='')
    create_time = models.DateTimeField(auto_now_add=True)

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
        return {
            'state': self.state,
            'value': self.power,
        }

    class Meta(object):
        verbose_name = verbose_name_plural = 'Ubung-1'
    
    def __str__(self):
        return f'{self.game.name} {self.player.name} {self.power}'

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
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='player')
    drainer = models.CharField(max_length=100, default='')
    create_time = models.DateTimeField(auto_now_add=True)

    @property
    def json(self):
        return {
            'game': self.game.link,
            'player': self.player.name,
            'drainer': self.drainer,
        }

    class Meta(object):
        verbose_name = verbose_name_plural = 'Ubung-3'
    
    def __str__(self):
        return f'{self.game.name} {self.player.name} {self.drainer}'

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

    class Meta(object):
        verbose_name = verbose_name_plural = 'Ubung-4'
    def __str__(self):
        return f'{self.game}---{self.player}'


class Ubung5(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='game')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='author')
    goal = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='goal',related_name='goal')
    score = models.IntegerField(default=0)


    @property
    def span_1(self):
        return {
            'id': self.player.id,
            'name': self.player.name,
            'avatar': self.player.avatar,
            'statusSide': self.score,
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



