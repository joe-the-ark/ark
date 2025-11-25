from meta.decorators import api, APIError
from .models import *
import requests
import json
import string
import random
import time
import hashlib
import re
import  urllib.parse
import base64
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.six import BytesIO

@api
def create_player(player_name, game_secret, gameName, inviter):

    player_name = urllib.parse.unquote(player_name)
    inviter = urllib.parse.unquote(inviter)

    player = Player.objects.filter(name=player_name, game_secret=game_secret, game_name=gameName, inviter_name=inviter).first()
    if not player:
        player = Player.objects.create(name=player_name, game_secret=game_secret, game_name=gameName, inviter_name=inviter)

    return {'code': 0, 'msg': '创建玩家成功'}

@api
def create_game(inviter, gameName, game_id):

    inviter = urllib.parse.unquote(inviter)

    player = Player.objects.filter(name=inviter, nickname=inviter, openid=game_id).first()
    if not player:
        player = Player.objects.create(name=inviter, game_secret=game_id, game_name=gameName, inviter_name=inviter, nickname=inviter, openid=game_id)

    game = Game.objects.filter(game_secret=game_id, game_name=gameName, inviter=player).first()
    if game:
        game.status = 1
        game.save()

    else:
        game = Game.objects.create(game_secret=game_id, game_name=gameName, inviter=player)

    return {'code': 0}


@api
def get_game_list(**params):

    games = Game.objects.filter(status=1)

    game_list = []
    for game in games:
        game_list.append([game.game_secret, game.game_name, game.inviter.name])

    return {'code': 0, 'gameList':game_list}


@api
def find_players(game_secret, gameName):
    players = Player.objects.filter(game_secret=game_secret, game_name=gameName)
    player_list = [ p.name for p in players]

    return {'code': 0, 'player_list': player_list}

@api
def get_player_list(game_secret, gameName, inviter):

    inviter = urllib.parse.unquote(inviter)


    players = Player.objects.filter(game_secret=game_secret, game_name=gameName, inviter_name=inviter)
    player_list = [ p.name for p in players ]

    return {'code': 0, 'player_list': player_list}


@api
def get_character_list():

    characters = [ _.name for _ in Character.objects.all()]

    return {'code': 0, 'characters': characters}

@api
def set_player_score(
    params, inviter_name, gameSecret, player, gameName,
    charaChooser, characterOne, characterTwo):


    inviter_name = urllib.parse.unquote(inviter_name)
    player = urllib.parse.unquote(player)

    inviter = Player.objects.filter(
        name=inviter_name,
        inviter_name=inviter_name,
        game_name=gameName,
        game_secret=gameSecret
    ).first()


    scorer = Player.objects.filter(
        name=player,
        inviter_name=inviter_name,
        game_name=gameName,
        game_secret=gameSecret
    ).first()

    charaChooser2 = Player.objects.filter(
        name=charaChooser,
        inviter_name=inviter_name,
        game_name=gameName,
        game_secret=gameSecret
    ).first()

    game = Game.objects.filter(
        game_secret=gameSecret,
        inviter=inviter,
        game_name=gameName,
        status=1
    ).first()

    character_one = Character.objects.filter(name=characterOne).first()
    character_two = Character.objects.filter(name=characterTwo).first()


    characterChoose = CharacterChoose.objects.filter(
        character_one = character_one,
        character_two = character_two,
        player=charaChooser2,
        game=game
    ).first()

    for k, v in params.items():
        _player = Player.objects.filter(
            name=k, game_secret=gameSecret, game_name=gameName, inviter_name=inviter_name
        ).first()


        playerScore = PlayerScore.objects.filter(
            character_choose=characterChoose,
            scorer=scorer,
            player=_player,
            game=game
        ).first()

        if playerScore:
            playerScore.score = v
            playerScore.save()
        else:
            PlayerScore.objects.create(
                character_choose=characterChoose,
                score=v,
                scorer=scorer,
                player=_player,
                game=game
            )

    return {'code':0, 'msg':'打分成功'}

@api
def save_character_choose(inviterName, gameSecret, playerName, gameName, charaChooser):

    inviterName = urllib.parse.unquote(inviterName)
    player = urllib.parse.unquote(playerName)

    character_one = Character.objects.filter(name=charaChooser[0]).first()
    character_two = Character.objects.filter(name=charaChooser[1]).first()

    player = Player.objects.filter(
        name=playerName, game_secret=gameSecret,
        inviter_name=inviterName, game_name=gameName
    ).first()

    inviter = Player.objects.filter(
        name=inviterName, inviter_name=inviterName,
        game_name=gameName, game_secret=gameSecret
    ).first()

    game = Game.objects.filter(
        game_secret=gameSecret, inviter=inviter,
        game_name=gameName, status=1
    ).first()


    cc = CharacterChoose.objects.filter(player=player, game=game).first()
    if cc:
        cc.character_one = character_one
        cc.character_two = character_two
        cc.save()
    else:
        CharacterChoose.objects.create(
            character_one=character_one, character_two=character_two,
            player=player, game=game
        )

    return {'code:':0}

@api
def get_player_score(inviter, gameName, gameSecret, player, character_one, character_two, chooser):

    inviter = urllib.parse.unquote(inviter)
    player = urllib.parse.unquote(player)

    _player = Player.objects.filter(
        name=player, game_secret=gameSecret,
        inviter_name=inviter, game_name=gameName
    ).first()

    _inviter = Player.objects.filter(
        name=inviter, game_secret=gameSecret,
        inviter_name=inviter, game_name=gameName
    ).first()

    chooser = Player.objects.filter(
        name=chooser, game_secret=gameSecret,
        inviter_name=inviter, game_name=gameName
    ).first()

    game = Game.objects.filter(
        game_secret=gameSecret,
        inviter=_inviter,
        game_name=gameName,
        status=1
    ).first()


    character_one = Character.objects.filter(name=character_one).first()
    character_two = Character.objects.filter(name=character_two).first()
    characterChoose = CharacterChoose.objects.filter(
        character_one=character_one, character_two=character_two,
        player=chooser, game=game
    ).first()

    player_scores = PlayerScore.objects.filter(game=game, player=_player, character_choose=characterChoose)

    player_list = []
    player_score_list = []

    for _ in player_scores:
        # if _.scorer.id == _player.id:
        #     continue
        player_list.append(_.scorer.name)
        player_score_list.append(int(_.score))

    _player_score_list = []


    for _ in player_scores:
        if _.scorer.id == _player.id:
            continue
        _player_score_list.append(_.score)


    if len(_player_score_list):
        middle = int(sum(list(map(int, _player_score_list))) / len(_player_score_list))
    else:
        middle = 0

    # player_list.append(player)
    # player_score_list.append(middle)

    return {'code':0, 'player_score_list':player_score_list, 'player_list': player_list, 'middle': middle}


@api
def get_player_characterlist(game_secret,inviter,player,gameName):

    inviter = urllib.parse.unquote(inviter)
    player = urllib.parse.unquote(player)

    _inviter = Player.objects.filter(
        name=inviter, inviter_name=inviter,
        game_name=gameName, game_secret=game_secret
    ).first()

    game = Game.objects.filter(
        game_secret=game_secret, inviter=_inviter,
        game_name=gameName, status=1
    ).first()

    cha_list = CharacterChoose.objects.filter(game=game)
    data = [ [_.player.name, [_.character_one.name, _.character_two.name]]  for _ in cha_list if cha_list]

    return {'code':0, 'data':data}


@api
def get_game_score(characterListParams, inviter, gameSecret, player, gameName):

    inviter = urllib.parse.unquote(inviter)
    player = urllib.parse.unquote(player)

    _player = Player.objects.filter(
        name=player, game_secret=gameSecret,
        inviter_name=inviter, game_name=gameName
    ).first()  # 取当前玩家名

    _inviter = Player.objects.filter(
        name=inviter, game_secret=gameSecret,
        inviter_name=inviter, game_name=gameName
    ).first()

    game = Game.objects.filter(
        game_secret=gameSecret,
        inviter=_inviter,
        game_name=gameName,
        status=1
    ).first()

    chooser_list = characterListParams[0]
    character_list = characterListParams[1]
    playercount = len(chooser_list)
    result_list = []
    player_scores = []

    # print('characterListParams:'+characterListParams)

    for index in range(0, playercount):

        result = [character_list[index][0], character_list[index][1]]
        chooser = Player.objects.filter(
            name=chooser_list[index], game_secret=gameSecret,
            inviter_name=inviter, game_name=gameName
        ).first()

        character_one = Character.objects.filter(name=character_list[index][0]).first()
        character_two = Character.objects.filter(name=character_list[index][1]).first()

        characterChoose = CharacterChoose.objects.filter(
            character_one=character_one, character_two=character_two,
            player=chooser, game=game
        ).first()

        player_scores = PlayerScore.objects.filter(game=game, player=_player, character_choose=characterChoose)
        count = player_scores.count()

        _player_score_list = []

        if count == playercount:
            player_score = 0
            for _ in player_scores:
                if _.scorer.id == _player.id:
                    player_score = _.score
                    # continue
                _player_score_list.append(_.score)

            middle = str(int(sum(list(map(int, _player_score_list))) / len(_player_score_list)))

            result.append(middle)
            result.append(player_score)

        result_list.append(result)

    _inviter = Player.objects.filter(
        name=inviter, game_secret=gameSecret,
        inviter_name=inviter, game_name=gameName
    ).first()

    game = Game.objects.filter(
        game_secret=gameSecret,
        inviter=_inviter,
        game_name=gameName,
        status=1
    ).first()

    players = Player.objects.filter(
        game_secret=gameSecret, inviter_name=inviter, game_name=gameName
    )
    ttsms = []
    for _player in players:

        chooser_list = characterListParams[0]
        character_list = characterListParams[1]
        playercount = len(chooser_list)

        middles = []
        for index in range(0, playercount):
            chooser = Player.objects.filter(
                name=chooser_list[index], game_secret=gameSecret,
                inviter_name=inviter, game_name=gameName
            ).first()
            character_one = Character.objects.filter(name=character_list[index][0]).first()
            character_two = Character.objects.filter(name=character_list[index][1]).first()
            characterChoose = CharacterChoose.objects.filter(
                character_one=character_one, character_two=character_two,
                player=chooser, game=game
            ).first()
            player_scores = PlayerScore.objects.filter(game=game, player=_player, character_choose=characterChoose)
            _player_score_list = []

            for _ in player_scores:
                _player_score_list.append(_.score)

            middle = int(sum(list(map(int, _player_score_list))) / len(_player_score_list))
            middles.append(middle)
        ttsms.append(str(int(sum(middles) / playercount)))


    return {'code':0, 'result': result_list, 'ttsms':ttsms}


@api
def save_players_process(inviter_name, game_secret, player, game_name, process, *args, **kwargs):

    inviter_name = urllib.parse.unquote(inviter_name)
    player = urllib.parse.unquote(player)

    _player = Player.objects.filter(
        name=player, game_secret=game_secret,
        inviter_name=inviter_name, game_name=game_name
    ).first()

    _inviter = Player.objects.filter(
        name=inviter_name, game_secret=game_secret,
        inviter_name=inviter_name, game_name=game_name
    ).first()

    game = Game.objects.filter(
        game_secret=game_secret,
        inviter=_inviter,
        game_name=game_name,
        status=1
    ).first()

    game_process = GameProcess.objects.filter(game=game, player=_player).first()
    if game_process:  # 之前存在的process
        game_process.process = process  # 赋值给新的game_process
        game_process.save()  # 保存进度

    else:  # 玩家没有进度的情况
        GameProcess.objects.create(game=game, player=_player, process=process)


@api
def get_players_process(game_secret, inviter_name, player, gameName):

    inviter_name = urllib.parse.unquote(inviter_name)
    player = urllib.parse.unquote(player)

    _player = Player.objects.filter(
        name=player, game_secret=game_secret,
        inviter_name=inviter_name, game_name=gameName
    ).first()

    _inviter = Player.objects.filter(
        name=inviter_name, game_secret=game_secret,
        inviter_name=inviter_name, game_name=gameName
    ).first()

    game = Game.objects.filter(
        game_secret=game_secret,
        inviter=_inviter,
        game_name=gameName,
        status=1
    ).first()

    playercount = Player.objects.filter(game_secret=game_secret, inviter_name=inviter_name, game_name=gameName).count()
    gameProcess = GameProcess.objects.filter(game=game, player=_player).first()

    if gameProcess:
        process = gameProcess.process
        if process == '0.1':
            firstScore = FirstScore.objects.filter(game=game, player=_player).first()
            playerScore = firstScore.first_score
            return {'code':0, 'playercount':playercount, 'playerScore':playerScore, 'process':process}

        if process == '0.2':
             return {'code':0, 'playercount':playercount, 'process':process}

    return {'code':0, 'process':'0.0'}

@api
def get_ttsm(characterListParams, inviter, gameSecret, player, gameName):

    inviter = urllib.parse.unquote(inviter)
    player = urllib.parse.unquote(player)

    _inviter = Player.objects.filter(
        name=inviter, game_secret=gameSecret,
        inviter_name=inviter, game_name=gameName
    ).first()

    game = Game.objects.filter(
        game_secret=gameSecret,
        inviter=_inviter,
        game_name=gameName,
        status=1
    ).first()

    players = Player.objects.filter(
        game_secret=gameSecret, inviter_name=inviter, game_name=gameName
    )

    ttsms = []
    for _player in players:

        chooser_list = characterListParams[0]
        character_list = characterListParams[1]
        playercount = len(chooser_list)

        middles = []
        for index in range(0, playercount):
            chooser = Player.objects.filter(
                name=chooser_list[index], game_secret=gameSecret,
                inviter_name=inviter, game_name=gameName
            ).first()

            character_one = Character.objects.filter(name=character_list[index][0]).first()
            character_two = Character.objects.filter(name=character_list[index][1]).first()
            characterChoose = CharacterChoose.objects.filter(
                character_one=character_one, character_two=character_two,
                player=chooser, game=game
            ).first()
            player_scores = PlayerScore.objects.filter(game=game, player=_player, character_choose=characterChoose)
            _player_score_list = []

            for _ in player_scores:
                _player_score_list.append(_.score)

            middle = int(sum(list(map(int, _player_score_list))) / len(_player_score_list))
            middles.append(middle)


        ttsms.append(str(int(sum(middles) / playercount)))

    return {'code':0, 'result':ttsms}


@api
def wechatapi(url):

    appid = 'wxc7594d7d49e0235f'
    secret = 'ebbda5cbab00241032bc936fe3839393'
    access_token_params = {
        'appid': appid,
        'secret': secret,
        'grant_type': 'client_credential'
    }
    get_access_token_url = 'https://api.weixin.qq.com/cgi-bin/token'

    response = requests.get(url=get_access_token_url, params=access_token_params)
    response.encoding = 'utf-8'
    response = json.loads(response.text)
    access_token = response['access_token']
    get_jsapi_ticket_url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={0}&type=jsapi'.format(access_token)

    jsapi_response = requests.get(url=get_jsapi_ticket_url)
    jsapi_response.encoding = 'utf-8'
    jsapi_response = json.loads(jsapi_response.text)
    jsapi_ticket = jsapi_response['ticket']

    noncestr = ''.join(random.sample(string.ascii_letters + string.digits, 8))

    timestamp = int(time.time())

    string1 = 'jsapi_ticket={0}&noncestr={1}&timestamp={2}&url={3}'.format(jsapi_ticket, noncestr, timestamp, url)
    signature = hashlib.sha1(string1.encode('utf-8')).hexdigest()

    params = {
        'appId': appid,
        'timestamp': timestamp,
        'nonceStr': noncestr,
        'signature': signature,
        'jsApiList': ['onMenuShareAppMessage', 'checkJsApi']

    }

    return {'code': 0, 'params': params}


@api
def firstvote(score, game_secret, inviter_name, player, gameName):

    inviter_name = urllib.parse.unquote(inviter_name)
    player = urllib.parse.unquote(player)

    print('inviter_name', inviter_name)
    print('player', player)

    _player = Player.objects.filter(
        name=player, game_secret=game_secret,
        inviter_name=inviter_name, game_name=gameName
    ).first()


    _inviter = Player.objects.filter(
        name=inviter_name, game_secret=game_secret,
        inviter_name=inviter_name, game_name=gameName
    ).first()

    game = Game.objects.filter(
        game_secret=game_secret,
        inviter=_inviter,
        game_name=gameName,
        status=1
    ).first()

    firstScore = FirstScore.objects.filter(game=game, player=_player).first()
    if firstScore:
        firstScore.first_score = score
        firstScore.save()

    else:
        FirstScore.objects.create(game=game, first_score=score, player=_player)

    return {'code':0}

@api
def getOthersSelfPerception(inviter_name, game_secret, player, gameName):

    inviter_name = urllib.parse.unquote(inviter_name)
    player = urllib.parse.unquote(player)

    _player = Player.objects.filter(
        name=player, game_secret=game_secret,
        inviter_name=inviter_name, game_name=gameName
    ).first()

    _inviter = Player.objects.filter(
        name=inviter_name, game_secret=game_secret,
        inviter_name=inviter_name, game_name=gameName
    ).first()

    game = Game.objects.filter(
        game_secret=game_secret,
        inviter=_inviter,
        game_name=gameName,
        status=1
    ).first()

    firstScore = FirstScore.objects.filter(game=game)
    OthersSelfPerceptionList = []
    for _ in firstScore:
        if _.player.id == _player.id:
            continue
        OthersSelfPerceptionList.append(int(_.first_score))

    return {'code':0, 'OthersSelfPerceptionList':OthersSelfPerceptionList}

@api
def getttsmindividual(inviter_name, game_secret, player, gameName, c1, c2, chooser):

    inviter_name = urllib.parse.unquote(inviter_name)
    player = urllib.parse.unquote(player)

    _player = Player.objects.filter(
        name=player, game_secret=game_secret,
        inviter_name=inviter_name, game_name=gameName
    ).first()

    _inviter = Player.objects.filter(
        name=inviter_name, game_secret=game_secret,
        inviter_name=inviter_name, game_name=gameName
    ).first()

    game = Game.objects.filter(
        game_secret=game_secret,
        inviter=_inviter,
        game_name=gameName,
        status=1
    ).first()


    chooser = Player.objects.filter(
        name=chooser, game_secret=game_secret,
        inviter_name=inviter_name, game_name=gameName
    ).first()


    players = Player.objects.filter(
        game_secret=game_secret, inviter_name=inviter_name, game_name=gameName
    )

    character_one = Character.objects.filter(name=c1).first()
    character_two = Character.objects.filter(name=c2).first()

    characterChoose = CharacterChoose.objects.filter(character_one=character_one, character_two=character_two, player=chooser, game=game).first()

    playerCount = Player.objects.filter(game_secret=game_secret,inviter_name=inviter_name, game_name=gameName).count()

    #找到所有已打分人
    playerScores =  PlayerScore.objects.filter(character_choose=characterChoose, game=game, player=_player)

    count = playerScores.count()


    #所有打分人的分数
    individualTensionScale = []
    for _ in playerScores:

        if _.scorer.id == _player.id:
            continue
        individualTensionScale.append(int(_.score))

    #当前scale所有人的itsm
    #   找到所有被打分人
    allttsm = 0
    for _ in playerScores:
        #被打分人 _.player
        #找到对_.player的所有playerScores
        playerScores2 =  PlayerScore.objects.filter(character_choose=characterChoose, game=game, player=_.player)
        count2 = playerScores2.count()
        #所有打分人的分数均数,不包括自己
        sumScore = 0
        for p in playerScores2:
            if p.scorer.id == _.player.id:
                continue
            sumScore += int(p.score)
        itsm2 = sumScore/count2
        allttsm += itsm2

    ttsm = int(allttsm/playerCount)

    return {'code':0, 'individualTensionScale':individualTensionScale, 'ttsm':ttsm, 'playerCount':playerCount}


@api
def getKeepUpVotingData(inviter_name, game_secret, player, gameName):

    inviter_name = urllib.parse.unquote(inviter_name)
    player = urllib.parse.unquote(player)

    #1、获取所有性格 2、所有人在该scale对该玩家评分的平均值 3、sp-itsm的差值的绝对值
    _player = Player.objects.filter(
        name=player, game_secret=game_secret,
        inviter_name=inviter_name, game_name=gameName
    ).first()


    _inviter = Player.objects.filter(
        name=inviter_name, game_secret=game_secret,
        inviter_name=inviter_name, game_name=gameName
    ).first()

    game = Game.objects.filter(
        game_secret=game_secret,
        inviter=_inviter,
        game_name=gameName,
        status=1
    ).first()


    characterChooses = CharacterChoose.objects.filter(game=game)

    simulatedData1 = []
    simulatedData2 = []
    for c in characterChooses:
        c1 = c.character_one.name
        c2 = c.character_two.name
        #根据该scale选择获取评分
        simulatedData = []

        playerScores = PlayerScore.objects.filter(character_choose=c, player=_player, game=game)
        othersCount = playerScores.count() - 1

        #其他人对该玩家的评分
        othersScoreList = []
        allttsm = 0
        sp = 0

        for _ in playerScores:

            if _.scorer.id == _player.id:
                sp = int(_.score)

                continue
            # else:
            othersScoreList.append(int(_.score))
        #其他人对该玩家的评分的均值
        average = sum(othersScoreList)
        if othersCount:
            itsm = int(average/othersCount)
        else:
            itsm = 0

        spitsm = abs(sp - itsm)


        #判断是不是玩家打分过的scale
        s2 = PlayerScore.objects.filter(character_choose=c, scorer=_player, game=game).first()
        simulatedData.append(c1)
        simulatedData.append(c2)
        simulatedData.append(itsm)
        simulatedData.append(spitsm)
        simulatedData.append(sp)


        if s2:
            simulatedData2.append(simulatedData)
        else:
            simulatedData1.append(simulatedData)


    return {'code':0, 'simulatedData1':simulatedData1, 'simulatedData2':simulatedData2}


@api
def getCharacterList(inviter_name, game_secret, player, gameName):
    inviter_name = urllib.parse.unquote(inviter_name)
    player = urllib.parse.unquote(player)

    #获取所有已经选择的性格

    _player = Player.objects.filter(
        name=player, game_secret=game_secret,
        inviter_name=inviter_name, game_name=gameName
    ).first()

    _inviter = Player.objects.filter(
        name=inviter_name, game_secret=game_secret,
        inviter_name=inviter_name, game_name=gameName
    ).first()

    game = Game.objects.filter(
        game_secret=game_secret,
        inviter=_inviter,
        game_name=gameName,
        status=1
    ).first()


    playerCount = Player.objects.filter(game_secret=game_secret, inviter_name=inviter_name, game_name=gameName).count()


    characterChooses = CharacterChoose.objects.filter(game=game)
    chooserList = []
    characterList = []
    for c in characterChooses:
        clist = []
        chooser = c.player.name
        character_one = c.character_one.name
        character_two = c.character_two.name

        chooserList.append(chooser)
        clist.append(character_one)
        clist.append(character_two)
        characterList.append(clist)

    result = []
    result.append(chooserList)
    result.append(characterList)


    players = Player.objects.filter(game_secret=game_secret, inviter_name=inviter_name, game_name=gameName)

    pscount = PlayerScore.objects.filter(game=game).count()
    check_score = 'false'
    if pscount == (playerCount * playerCount) * playerCount:
        check_score = 'true'

    return {'code':0, 'characterListParams':result, 'playerCount':playerCount,'check_score':check_score}


@api
def wechatlogin(**params):

    code = params['code']

    appid = 'wxc7594d7d49e0235f'
    secret = 'ebbda5cbab00241032bc936fe3839393'
    #获取access_token、openid
    access_token_params = {
        'appid': appid,
        'secret': secret,
        'code': code,
        'grant_type': 'authorization_code'
    }
    get_access_token_url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
    response = requests.get(url=get_access_token_url, params=access_token_params)
    response.encoding = 'utf-8'

    response = json.loads(response.text)

    access_token = response['access_token']
    openid = response['openid']
        #获取用户信息
    get_user_info_url = 'https://api.weixin.qq.com/sns/userinfo'
    user_info_params = {
        'access_token': access_token,
        'openid': openid
    }
    res = json.loads(requests.get(url=get_user_info_url, params=user_info_params).text)

    openid = res['openid']

    nickname = res['nickname'].encode('raw_unicode_escape').decode()
    #判断用户账号是否存在
    user_data = {
        'nickname': nickname,
        'openid': res['openid']
    }

    if 'inviter' in params.keys():
        inviter = urllib.parse.unquote(params['inviter'])
        game_secret = params['game_secret']
        game_name = params['game_name']

        player = Player.objects.filter(name=nickname, inviter_name=inviter, game_secret=game_secret, game_name=game_name, nickname=nickname, openid=openid).first()
        if not player:
            player = Player.objects.create(name=nickname, inviter_name=inviter, game_secret=game_secret, game_name=game_name, nickname=nickname, openid=openid)

    return {'code':0, 'result':user_data}

    # user = User.objects.filter(unionid=unionid).first()
    # if user:
    #     if not user.mobile:
    #         return {'msg': '当前用户未注册账号,转至注册页面', 'code': 1, 'user_data':user_data}

    #     return {'msg': '当前用户已注册账号，可直接登录', 'code': 0, 'user_data': user_data}

    # #账号注册页面
    # else:
    #     User.objects.create(
    #         nickname=res['nickname'].encode('raw_unicode_escape').decode(),
    #         sex=res['sex'],
    #         province=res['province'].encode('raw_unicode_escape').decode(),
    #         city=res['city'].encode('raw_unicode_escape').decode(),
    #         country=res['country'].encode('raw_unicode_escape').decode(),
    #         headimgurl=res['headimgurl'],
    #         unionid=res['unionid'],
    #         username='1'
    #     )
    #     return {'msg': '当前用户未注册账号,转至注册页面', 'code': 1, 'user_data':user_data}

@api
def getPlayerList(**params):

    inviter_name = urllib.parse.unquote(params['inviter_name'])
    game_secret = params['game_secret']
    gameName = params['gameName']

    playerList = Player.objects.filter(
        game_secret=game_secret,
        game_name = gameName,
        inviter_name = inviter_name
    )

    nicknameList = []
    for _ in playerList:
        nicknameList.append(_.nickname)
    return {'code':0, 'result':nicknameList}


@api
def getGameStatus(**params):

    inviter_name = urllib.parse.unquote(params['inviter_name'])
    game_secret = params['game_secret']
    gameName = params['gameName']
    openid = params['openid']
    nickname = urllib.parse.unquote(params['nickname'])

    print('getGameStatus:', params)

    _player = Player.objects.filter(name=nickname, game_secret=game_secret, inviter_name=inviter_name, game_name=gameName).first()

    _inviter = Player.objects.filter(
        name=inviter_name, game_secret=game_secret,
        inviter_name=inviter_name, game_name=gameName
    ).first()

    print(_inviter)

    game = Game.objects.filter(
        game_secret=game_secret,
        inviter=_inviter,
        game_name=gameName,
    ).first()

    if game.status == 0:
        return {'code':0, 'result':0}

    if game.status == 1:
        if _player:
            return {'code':0, 'result':1} #游戏已开始之前，玩家已被记录
        return {'code':0, 'result':2} #游戏已开始前，玩家没被记录，不能进游戏

    if game.status == 2:
        return {'code':0, 'result': 3} #游戏结束


@api
def push_feedback(game_secret, gameName, player, inviter_name, love, add, ask, teammate):

    inviter_name = urllib.parse.unquote(inviter_name)
    player = urllib.parse.unquote(player)

    _inviter = Player.objects.filter(
        name=inviter_name,
        game_secret=game_secret,
        inviter_name=inviter_name,
        game_name=gameName
    ).first()

    game = Game.objects.filter(
        game_secret=game_secret,
        game_name=gameName,
        inviter=_inviter,
    ).first()

    _teammate = Player.objects.filter(
        name=teammate,
        game_secret=game_secret,
        game_name=gameName,
        inviter_name=inviter_name
    ).first()

    _player = Player.objects.filter(
        name=player,
        game_secret=game_secret,
        game_name=gameName,
        inviter_name=inviter_name
    ).first()

    feedback = Feedback.objects.filter(game=game, player=_player, teammate=_teammate).first()
    if not feedback:
        Feedback.objects.create(love=love, add=add, ask=ask, game=game, player=_player, teammate=_teammate)

    feedbacks = Feedback.objects.filter(teammate=_player, game=game)

    loveFeedback = []
    addFeedback = []
    askFeedback = []

    result = []

    for _ in feedbacks:

        love = cut_text(_.love, 30)
        love.append('')
        loveFeedback += love

        add = cut_text(_.add, 30)
        add.append('')
        addFeedback += add

        ask = cut_text(_.ask, 30)
        ask.append('')
        askFeedback += ask

    result.append(loveFeedback)
    result.append(addFeedback)
    result.append(askFeedback)
    return {'code':0, 'result':result}



@api
def get_players(inviter, game_secret, gameName, player):

    inviter = urllib.parse.unquote(inviter)
    player = urllib.parse.unquote(player)

    player_list = Player.objects.filter(
        game_secret=game_secret,
        game_name=gameName,
        inviter_name=inviter
    )

    result = []
    for p in player_list:
        if p.name == player:
            continue

        result.append(p.name)

    return {'code':0, 'result':result}



def cut_text(text, lenth):
    textArr = re.findall('.{'+str(lenth)+'}', text)
    textArr.append(text[(len(textArr)*lenth):])
    return textArr

@api
def getOthersFeedback(inviter, game_secret, gameName, player):

    inviter = urllib.parse.unquote(inviter)
    player = urllib.parse.unquote(player)

    _player = Player.objects.filter(
        name=player,
        game_secret=game_secret,
        game_name=gameName,
        inviter_name=inviter
    ).first()

    _inviter = Player.objects.filter(
        name=inviter,
        game_secret=game_secret,
        inviter_name=inviter,
        game_name=gameName
    ).first()

    game = Game.objects.filter(
        game_secret=game_secret,
        game_name=gameName,
        inviter=_inviter,
    ).first()

    feedbacks = Feedback.objects.filter(teammate=_player, game=game)

    loveFeedback = []
    addFeedback = []
    askFeedback = []

    result = []

    for _ in feedbacks:

        love = cut_text(_.love, 30)
        love.append('')
        loveFeedback += love

        add = cut_text(_.add, 30)
        add.append('')
        addFeedback += add

        ask = cut_text(_.ask, 30)
        ask.append('')
        askFeedback += ask


    result.append(loveFeedback)
    result.append(addFeedback)
    result.append(askFeedback)

    return {'code':0, 'result':result}


@api
def game_end(inviter_name, game_secret, gameName, player):

    inviter_name = urllib.parse.unquote(inviter_name)
    player = urllib.parse.unquote(player)

    _inviter = Player.objects.filter(
        name=inviter_name,
        game_secret=game_secret,
        inviter_name=inviter_name,
        game_name=gameName
    ).first()

    game = Game.objects.filter(
        game_secret=game_secret,
        game_name=gameName,
        inviter=_inviter,
    ).first()

    flag = True

    players = Player.objects.filter(game_name=gameName, game_secret=game_secret, inviter_name=inviter_name)
    for p in players:
        process = GameProcess.objects.filter(game=game, player=p).first()
        if process.process != '10':
            flag = False

    if flag:
        Player.objects.filter(game_secret=game_secret, game_name=gameName, inviter_name=inviter_name).delete()


    return {'code':0}


@api
def check_game(inviter_name, game_name, game_secret):

    inviter_name = urllib.parse.unquote(inviter_name)

    _inviter = Player.objects.filter(
        name=inviter_name,
        game_secret=game_secret,
        inviter_name=inviter_name,
        game_name=game_name
    ).first()

    game = Game.objects.filter(
        game_secret=game_secret,
        game_name=game_name,
        inviter=_inviter,
    ).first()

    if game:
        return {'gameExist':0}
    else:

        return {'gameExist':1}


@api
def save_result(base64Str, player, name, game_secret, inviter):
    imgdata = base64.b64decode(base64Str[22:]+'==')
    file = BytesIO()
    file.write(imgdata)
    img = InMemoryUploadedFile(file, None, 'result.jpg', None, len(imgdata), None, None)
    result = Result.objects.filter(player=player,name=name, game_secret=game_secret, inviter=inviter).first()
    if not result:
        Result.objects.create(img=img,player=player, name=name, game_secret=game_secret, inviter=inviter)

    else:
        result.img = img
        result.save()



@api
def check_game_point(inviter_name, game_secret, player, game_name):
    inviter_name = urllib.parse.unquote(inviter_name)
    player = urllib.parse.unquote(player)
    _inviter = Player.objects.filter(
        name=inviter_name,
        game_secret=game_secret,
        inviter_name=inviter_name,
        game_name=game_name
    ).first()

    game = Game.objects.filter(
        game_secret=game_secret,
        game_name=game_name,
        inviter=_inviter,
    ).first()

    _player = Player.objects.filter(
        name=player,
        game_secret=game_secret,
        game_name=game_name,
        inviter_name=inviter_name
    ).first()

    players_count = Player.objects.filter(game_name=game_name, game_secret=game_secret, inviter_name=inviter_name).count()
    feedback_count = Feedback.objects.filter(teammate=_player, game=game).count()
    print('players_count',players_count)
    print('feedback_count',feedback_count)


    playerVotedCount = Feedback.objects.filter(player=_player, game=game).count()
    print('playerVotedCount',playerVotedCount)

    if players_count-1 == playerVotedCount:

        if players_count-1 == feedback_count:
            print('code=0')
            return {'code':0, 'msg':'投票完毕'}
        else:
            print('code=1')
            return {'code':1, 'mgs':'其他玩家没投完'}
    else:
        print('code=2')
        return {'code':2, 'mgs':'正常情况'}





























