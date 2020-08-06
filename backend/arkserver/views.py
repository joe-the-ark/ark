from django.shortcuts import render

# Create your views here.
from .models import *

def result(request, name, player, game_secret, inviter):

    ctx = {}
    ctx['results'] = Result.objects.filter(player=player, game_secret=game_secret, inviter=inviter)
    print(ctx['results'])

    _player = Player.objects.filter(
        name=player,
        game_secret=game_secret,
        inviter_name=inviter
    ).first()

    _inviter = Player.objects.filter(
        name=inviter,
        game_secret=game_secret,
        inviter_name=inviter,
    ).first()

    game = Game.objects.filter(
        game_secret=game_secret,
        inviter=_inviter,
    ).first()

    feedbacks = Feedback.objects.filter(teammate=_player, game=game)

    loveFeedback = []
    addFeedback = []
    askFeedback = []

    for feedback in feedbacks:
        loveFeedback.append(feedback.love)
        addFeedback.append(feedback.add)
        askFeedback.append(feedback.ask)

    ctx['loveFeedback'] = loveFeedback
    ctx['addFeedback'] = addFeedback
    ctx['askFeedback'] = askFeedback

    return render(request, 'result.html', ctx)



def index(request):
    ctx = {}
    return render(request,'./index.html', ctx)

def auth(request):
    ctx = {}

    if request.method == 'POST':
        username = request.POST.get('Nutzername')
        gamename = request.POST.get('name-des-spiels')
        avatar = request.POST.get('avatar')
        link = request.POST.get('link')

    return render(request,'./views/auth.html', ctx)

def auth_link(request):
    ctx = {}

    if request.method == 'POST':
        username = request.POST.get('Nutzername')
        avatar = request.POST.get('name-des-spiels')
        gamename = request.POST.get('name-des-spiels')
        link = request.POST.get('link')

    return render(request,'./views/auth-link.html', ctx)

def preview(request):
    ctx = {}
    return render(request, './views/preview.html', ctx)

def ubung_1(request):
    ctx = {}
    return render(request, './views/ubung-1.html', ctx)

def ubung_2(request):
    ctx = {}
    return render(request, './views/ubung-2.html', ctx)

def ubung_3(request):
    ctx = {}
    return render(request, './views/ubung-3.html', ctx)

def ubung_4(request):
    ctx = {}
    return render(request, './views/ubung-4.html', ctx)

def ubung_5(request):
    ctx = {}
    return render(request, './views/ubung-5.html', ctx)

def team_potential(request):
    ctx = {}
    return render(request, './views/team-potential.html', ctx)

def spannungsfelder(request):
    ctx = {}
    return render(request, './views/spannungsfelder.html', ctx)

def preview_2(request):
    ctx = {}
    return render(request, './views/preview-2.html', ctx)

def mission_2_ubung_1(request):
    ctx = {}
    return render(request, './views/mission-2-ubung-1.html', ctx)

def mission_2_ubung_2(request):
    ctx = {}
    return render(request, './views/mission-2-ubung-2.html', ctx)

def assessment(request):
    ctx = {}
    return render(request, './views/assessment.html', ctx)

def goodbye(request):
    ctx = {}
    return render(request, './views/goodbye.html', ctx)

def arche(request):
    ctx = {}
    return render(request, './views/arche.html', ctx)

def wartezimmer(request):
    ctx = {}
    return render(request, './views/wartezimmer.html', ctx)

def psychologischer(request):
    ctx = {}
    return render(request, './views/psychologischer.html', ctx)

