"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import meta
from django.conf.urls.static import static
from django.conf import settings
from arkserver import views as server_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', meta.urls),
    path('', include(meta.urls)),
    path('', server_views.index),
    path('auth/',server_views.auth),
    path('auth-link/',server_views.auth_link),
    path('<str:link>/',server_views.link_enter),

    path('preview/',server_views.preview),
    path('ubung-1/',server_views.ubung_1),
    path('ubung-2/',server_views.ubung_2),
    path('ubung-3/',server_views.ubung_3),
    path('ubung-4/',server_views.ubung_4),
    path('ubung-5/',server_views.ubung_5),
    path('team-potential/',server_views.team_potential),
    path('spannungsfelder/',server_views.spannungsfelder),
    path('preview-2/',server_views.preview_2),
    path('mission-2-ubung-1/',server_views.mission_2_ubung_1),
    path('mission-2-ubung-2/',server_views.mission_2_ubung_2),
    path('assessment/',server_views.assessment),
    path('goodbye/',server_views.goodbye),
    path('arche/',server_views.arche),
    path('wartezimmer/',server_views.wartezimmer),
    path('psychologischer/',server_views.psychologischer),
    path('logout/', server_views.logout),
    # path('wartezimmer/<str:link>/', server_views.wartezimmer),


    # path('', restapi.vue()),
    path('result/<str:name>/<str:player>/<str:game_secret>/<str:inviter>/', server_views.result),

] 
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.LOCAL:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
