from django.shortcuts import render

from meta.decorators import user_required


@user_required
def home(request, user):
    return render(request, 'home.html')
