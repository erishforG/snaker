from django.conf.urls import url
from shortner.views import shortener_view


urlpatterns = [

    # tracker
    url(r'^/?$', shortener_view.url_list_controller, name='url_list_controller'),

    url(r'^create/$', shortener_view.url_create_controller, name='url_create_controller'),

    url(r'^(?P<hash>\w+)/info/$', shortener_view.url_detail_controller, name='url_detail_controller'),

    url(r'^(?P<hash>\w+)/info/day/$', shortener_view.daily_source_controller, name='daily_source_download'),

    url(r'^download/$', shortener_view.url_list_download_controller, name="url_list_download"),

]