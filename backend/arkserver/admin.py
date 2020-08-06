from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Player)
admin.site.register(Game)
admin.site.register(Character)
admin.site.register(CharacterChoose)
admin.site.register(PlayerScore)
admin.site.register(GameProcess)
admin.site.register(FirstScore)
admin.site.register(Feedback)
admin.site.register(Result)

