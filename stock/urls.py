from django.conf.urls import url
from . import views

urlpatterns = [

    # /stock/
    url(r'^$', views.first, name='home'),


    # /stock/<pk>/
    url(r'^(?P<pid>[0-9]+)/$', views.detailview, name='detail'),

    # /stock/<pk>/addtolist
    url(r'^(?P<pid>[0-9]+)/addtolist/$', views.addtolist, name='addtolist'),

    # /stock/<pk>/remove
    url(r'^(?P<pid>[0-9]+)/remove/$', views.remove, name='remove'),

    # /stock/about/
    url(r'^about/$', views.about, name='about'),

    # /stock/services/
    url(r'^services/$', views.services, name='services'),

    # /stock/contact/
    url(r'^contact/$', views.contact, name='contact'),


    # /stock/dashboard/
    url(r'^dashboard/$', views.dashboard, name='dashboard'),

    # /stock/search/
    url(r'^search/$', views.search, name='search'),

    # /stock/noti/
    url(r'^noti/$', views.noti, name='noti'),

    # /stock/profile/
    url(r'^profile/$', views.paaa, name='profile'),

    # /stock/profile/edit/
    url(r'^profile/edit/$', views.edit, name='edit'),

    # /stock/register/
    url(r'^register/$', views.profileregister, name='register'),

    # /stock/logout/
    url(r'^logout/$', views.logout_view, name='logout'),

    # /stock/register/bakwas/
    url(r'^register/bakwas/$', views.gita, name=''),





    # /stock/all/
    url(r'^all/$', views.listview, name='all'),


    # /stock/feed/
    #url(r'^feed/$', views.git, name='33rwdfwefefewefwefwf'),

    # /stock/all/(0,1,2)/<page no>/
    url(r'^all/(?P<fby>[0-5]{1})/(?P<page>[0-9]+)/$', views.pagi, name='k'),

]
