from django.db import models

# Create your models here.

class Player(models.Model):
    name = models.CharField(max_length=100, verbose_name='player_name')
    nickname = models.CharField(max_length=100, verbose_name='nickname', default='')
    openid = models.CharField(max_length=100, verbose_name='openid', default='')
    game_secret = models.CharField(max_length=200, verbose_name='game_password', null=True, blank=True)
    game_name = models.CharField(max_length=200, verbose_name='game_name')
    inviter_name = models.CharField(max_length=200, verbose_name='creater')


    class Meta(object):
            verbose_name = verbose_name_plural = 'players'

    def __str__(self):
        return self.name

class Game(models.Model):
    game_secret = models.CharField(max_length=200, verbose_name='game_password', null=True, blank=True)
    game_name = models.CharField(max_length=200, verbose_name='game_name')
    inviter = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='creater', related_name='inviter_game')
    status = models.IntegerField(
        default=0,
        choices=((0, 'start'), (1, 'running'), (2, 'end')),
        verbose_name='game_status'
    )

    class Meta(object):
            verbose_name = verbose_name_plural = 'games'

    def __str__(self):
        return 'name:' + self.game_name + '，' + 'inviter:'+self.inviter.name

class Character(models.Model):
    name = models.CharField(max_length=100, verbose_name='scale')

    class Meta(object):
            verbose_name = verbose_name_plural = 'scales'

    def __str__(self):
        return self.name

class CharacterChoose(models.Model):
    character_one = models.ForeignKey(Character, on_delete=models.CASCADE, verbose_name='scale_one', related_name='character_one')
    character_two = models.ForeignKey(Character, on_delete=models.CASCADE, verbose_name='scale_two', related_name='character_two')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='chooser')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='game')
    status = models.IntegerField(
        default=0,
        choices=((0, 'nomal'), (1, 'showed')),
        verbose_name='status'
    )

    class Meta(object):
            verbose_name = verbose_name_plural = 'tension_scale'

    def __str__(self):
        return self.character_one.name +','+self.character_two.name

class PlayerScore(models.Model):
    character_choose = models.ForeignKey('CharacterChoose', on_delete=models.CASCADE)
    score = models.CharField(max_length=100, verbose_name='score')
    scorer = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='voting_person', related_name='scorer_score')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='voted_person', related_name='player_score')
    game = models.ForeignKey('Game', on_delete=models.CASCADE, verbose_name='game')

    class Meta(object):
            verbose_name = verbose_name_plural = 'voting'

    def __str__(self):
        return self.player.name + ':'+ self.score


class GameProcess(models.Model):

    class Meta(object):
        verbose_name = verbose_name_plural = 'progress'

    game = models.ForeignKey('Game', on_delete=models.CASCADE, verbose_name='game')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='player')
    process = models.CharField(max_length=100, verbose_name='progress')

    def __str__(self):
        return self.game.game_name+'__'+self.player.name+'__'+self.process


class FirstScore(models.Model):
    class Meta(object):
        verbose_name = verbose_name_plural = 'first score'

    first_score = models.CharField(max_length=20, verbose_name='first score')
    game = game = models.ForeignKey('Game', on_delete=models.CASCADE, verbose_name='game')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='player')


    def __str__(self):
        return self.player.name + '__firstScore:'+self.first_score


class Feedback(models.Model):
    love = models.CharField(max_length=500, verbose_name='love')
    add = models.CharField(max_length=500, verbose_name='add')
    ask = models.CharField(max_length=500, verbose_name='ask')
    
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='player', related_name='player')
    teammate = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='teammate', related_name='teammate')
    game = models.ForeignKey('Game', on_delete=models.CASCADE, verbose_name='game')

    def __str__(self):
        return self.game.game_name+'__'+self.player.name


class Result(models.Model):
    name = models.CharField(max_length=500,default='')
    player = models.CharField(max_length=500,default='')
    game_secret = models.CharField(max_length=500, default='')
    inviter = models.CharField(max_length=100, default='')
    img = models.FileField(upload_to='result/')



