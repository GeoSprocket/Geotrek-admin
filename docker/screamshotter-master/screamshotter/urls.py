from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$',  include('screamshot.urls', namespace='screamshot', app_name='screamshot')),
)
