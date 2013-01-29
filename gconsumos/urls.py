from dajaxice.core import dajaxice_config, dajaxice_autodiscover
from django.conf.urls import patterns, include, url


# Uncomment the next two lines to enable the admin:
from django.contrib import admin


admin.autodiscover()
dajaxice_autodiscover()

urlpatterns = patterns('',
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    (r'^ajax_select/', include('ajax_select.urls')),
    (r'^$', 'django.contrib.auth.views.login'),
    url(r'^inicio/', 'web.views.inicio', name='inicio'),
    url(r'^general/generales/$', 'web.views.generales', name='generales'),
    url(r'^general/configuracion/$', 'web.views.configuracion', name='configuracion'),
    url(r'general/ptsmedidas/(?P<pk>\d+)/$','web.views.ptsmedidasEdita',name='ptsmedidasEdita'),
    url(r'general/ptsmedidas/$','web.views.ptsmedidas',name='ptsmedidas'),
    url(r'general/ptsmedidas/del/(?P<pk>\d+)/$','web.views.ptsmedidasDelete',name='ptsmedidasDelete'),
    url(r'general/ptsmedidas/add/$','web.views.ptsmedidasNuevo',name='ptsmedidasNuevo'),
    url(r'panelcontrol/alarmas/(?P<pk>\d+)/$','web.views.alarmasEdita',name='alarmasEdita'),
    url(r'panelcontrol/alarmas/$','web.views.alarmas',name='alarmas'),
    url(r'panelcontrol/alarmas/del/(?P<pk>\d+)/$','web.views.alarmasDelete',name='alarmasDelete'),
    url(r'panelcontrol/alarmas/add/$','web.views.alarmasNuevo',name='alarmasNuevo'),
    url(r'panelcontrol/logs/$','web.views.verLogs',name='leerlogs'),
    url(r'lecturas/ultimas/(?P<tipo>\d+)/$','web.views.lecturas',name='lecturas'),
    (r'^test/','web.views.test'),
    url(r'^admin/', include(admin.site.urls)),
)


