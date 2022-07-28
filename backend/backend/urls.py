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

from django.views.generic import RedirectView

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    # path('api/', meta.urls),
    path('', include(meta.urls)),
    # path('', server_views.index),
    path('', server_views.auth),


    path('auth/',RedirectView.as_view(url='/initiate')),
    path('auth-link/',RedirectView.as_view(url='/onboard')),
    path('link/<str:link>/',server_views.link_enter),

    path('preview/',RedirectView.as_view(url='/first-mission')),
    path('ubung-2/',RedirectView.as_view(url='/team-potential')),
    path('ubung-1/',RedirectView.as_view(url='/energy-source')),
    path('ubung-3/',RedirectView.as_view(url='/energy-drainer')),
    path('wartezimmer/',RedirectView.as_view(url='/waiting-room')),
    path('ubung-5/',RedirectView.as_view(url='/team-tensions')),
    path('ubung-4/',RedirectView.as_view(url='/safety-score')),
    # path('waiting_room2/',RedirectView.as_view(url='/waiting-room2')),
    path('psychologischer/',RedirectView.as_view(url='/safety-result')),
    path('team-potential-/',RedirectView.as_view(url='/potential-result')),
    path('spannungsfelder/',RedirectView.as_view(url='/tensions-result')),
    path('preview-2/',RedirectView.as_view(url='/second-mission')),
    path('mission-2-ubung-1/',RedirectView.as_view(url='/social-sensitivity')),
    path('mission-2-ubung-2/',RedirectView.as_view(url='/development-feedbacks')),
    # path('waiting_room3/',RedirectView.as_view(url='/waiting-room3')),
    path('assessment/',RedirectView.as_view(url='/game-insights')),
    path('goodbye/',server_views.goodbye),
    path('arche/',RedirectView.as_view(url='/farewell')),
    path('logout/', server_views.logout),
      

    path('initiate/',server_views.auth),
    path('onboard/',server_views.auth_link),
    path('first-mission/',server_views.preview),
    path('team-potential/',server_views.ubung_2),
    path('energy-source/',server_views.ubung_1),
    path('energy-drainer/',server_views.ubung_3),
    path('waiting-room/',server_views.wartezimmer),
    path('team-tensions/',server_views.ubung_5),
    path('safety-score/',server_views.ubung_4),
    path('waiting-room2/',server_views.waiting_room2),
    path('safety-result/',server_views.psychologischer),
    path('potential-result/',server_views.team_potential),
    path('tensions-result/',server_views.spannungsfelder),
    path('heatmap/', server_views.heatmap),
    path('second-mission/',server_views.preview_2),
    path('social-sensitivity/',server_views.mission_2_ubung_1),
    path('development-feedbacks/',server_views.mission_2_ubung_2),
    path('waiting-room3/', server_views.waiting_room3),
    path('game-insights/',server_views.assessment),
    path('farewell/',server_views.arche),

    
    
    # path('', restapi.vue()),
    path('result/<str:name>/<str:player>/<str:game_secret>/<str:inviter>/', server_views.result),


]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.LOCAL:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
