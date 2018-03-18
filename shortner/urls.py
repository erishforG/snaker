from django.conf.urls import url

from shortner.views import shortner_view

urlpatterns = [

    # tracker
    url(r'^/?$', shortner_view.url_list_controller, name='url_list_controller'),

    url(r'^create/$', shortner_view.url_create_controller, name='url_create_controller'),

    url(r'^(?P<hash>\w+)/info/$', shortner_view.url_detail_controller, name='url_detail_controller'),

    url(r'^(?P<hash>\w+)/info/downdaily/$', shortner_view.daily_source_download, name='daily_source_download'),

    url(r'^download/$', shortner_view.url_list_download, name="url_list_download"),

]