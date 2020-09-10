from django.contrib import admin
from django.contrib.auth.models import User as AuthUser, Group as AuthGroup

from .models import User, WechatUser, MiniappUser, PublicAccountUser, MiniappTicket, Token


admin.site.site_header = admin.site.site_title = 'META'

admin.site.unregister(AuthUser)
admin.site.unregister(AuthGroup)

admin.site.register(User)
admin.site.register(WechatUser)
admin.site.register(MiniappUser)
admin.site.register(PublicAccountUser)
admin.site.register(MiniappTicket)
admin.site.register(Token)

