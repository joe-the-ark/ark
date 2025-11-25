from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Player)
admin.site.register(Game)
admin.site.register(WaitingRoomMember)
admin.site.register(Ubung1)
admin.site.register(Ubung2)
admin.site.register(Ubung3)
admin.site.register(Ubung4)
# admin.site.register(Ubung5)

class Ubung5Admin(admin.ModelAdmin):
    list_display = ['game', 'player', 'goal', 'score', 'ubung1', 'ubung3']
    # ordering = ['-time']

admin.site.register(Ubung5, Ubung5Admin)


admin.site.register(M2Ubung1)
admin.site.register(M2Ubung2)
admin.site.register(LastStop)
admin.site.register(Waitingroom2)




# admin.site.register(Ubung4)
# admin.site.register(Character)
# admin.site.register(CharacterChoose)
# admin.site.register(PlayerScore)
# admin.site.register(GameProcess)
# admin.site.register(FirstScore)
# admin.site.register(Feedback)
# admin.site.register(Result)

